"""Dashboard API routes."""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from ..db.database import get_db
from ..db.models import Shop, DailyRollup, Order
from ..auth.middleware import get_current_shop
from ..services.profit_calculator import ProfitCalculator
from ..utils.time_periods import get_time_period_dates

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
profit_calculator = ProfitCalculator()


@router.get("/summary")
async def get_dashboard_summary(
    period: str = Query("today", description="Time period: today, yesterday, 7d, mtd"),
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard summary for a time period."""
    try:
        # Get date range for period
        date_range = get_time_period_dates(period, shop.timezone)
        
        # Get daily rollups for the period
        result = await db.execute(
            select(DailyRollup)
            .where(
                and_(
                    DailyRollup.shop_id == shop.id,
                    DailyRollup.date >= date_range['start'].date(),
                    DailyRollup.date <= date_range['end'].date()
                )
            )
            .order_by(DailyRollup.date)
        )
        rollups = result.scalars().all()
        
        # Calculate totals
        total_net_revenue = sum(rollup.net_revenue for rollup in rollups)
        total_cogs = sum(rollup.cogs for rollup in rollups)
        total_fees = sum(rollup.fees for rollup in rollups)
        total_shipping_cost = sum(rollup.shipping_cost for rollup in rollups)
        total_ad_spend = sum(
            sum(rollup.ad_spend.values()) if rollup.ad_spend else 0 
            for rollup in rollups
        )
        total_net_profit = sum(rollup.net_profit for rollup in rollups)
        
        # Calculate margin percentage
        margin_pct = (total_net_profit / total_net_revenue * 100) if total_net_revenue > 0 else 0
        
        # Get order count and AOV
        order_result = await db.execute(
            select(func.count(Order.id), func.avg(Order.current_total_price))
            .where(
                and_(
                    Order.shop_id == shop.id,
                    Order.processed_at >= date_range['start'],
                    Order.processed_at <= date_range['end']
                )
            )
        )
        order_count, avg_order_value = order_result.first()
        
        # Calculate data health score
        health_score = await _calculate_data_health_score(db, shop, date_range)
        
        return {
            "period": period,
            "net_revenue": float(total_net_revenue),
            "cogs": float(total_cogs),
            "fees": float(total_fees),
            "shipping_cost": float(total_shipping_cost),
            "ad_spend": float(total_ad_spend),
            "net_profit": float(total_net_profit),
            "margin_pct": float(margin_pct),
            "orders_count": order_count or 0,
            "aov": float(avg_order_value) if avg_order_value else 0,
            "computed_at": datetime.utcnow().isoformat(),
            "currency": shop.currency,
            "flags": {
                "fees_estimated": total_fees > 0 and any(
                    any(rollup.ad_spend.values()) if rollup.ad_spend else False 
                    for rollup in rollups
                ),
                "missing_costs": health_score < 0.8,
                "data_health_score": health_score
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard summary: {str(e)}")


@router.get("/orders/{order_id}")
async def get_order_detail(
    order_id: str,
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed order information with profit breakdown."""
    # Get order with all related data
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.lines),
            selectinload(Order.refunds),
            selectinload(Order.transactions).selectinload(Transaction.fees)
        )
        .where(
            and_(
                Order.shop_id == shop.id,
                Order.shop_order_id == order_id
            )
        )
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Calculate profit breakdown
    profit_data = await profit_calculator.calculate_order_profit(db, order)
    
    return {
        "order": {
            "id": str(order.id),
            "shop_order_id": order.shop_order_id,
            "created_at": order.created_at.isoformat(),
            "processed_at": order.processed_at.isoformat(),
            "currency": order.currency,
            "presentment_currency": order.presentment_currency,
            "total_price": float(order.current_total_price),
            "total_discounts": float(order.current_total_discounts),
            "total_tax": float(order.current_total_tax),
            "financial_status": order.financial_status,
            "fulfillment_status": order.fulfillment_status,
            "flags": order.flags
        },
        "lines": [
            {
                "id": str(line.id),
                "line_id": line.line_id,
                "product_id": line.product_id,
                "variant_id": line.variant_id,
                "quantity": line.quantity,
                "price": float(line.price_set.get('shop_money', {}).get('amount', 0)),
                "unit_cost": float(line.effective_unit_cost) if line.effective_unit_cost else None,
                "cost_source": line.cost_source
            }
            for line in order.lines
        ],
        "refunds": [
            {
                "id": str(refund.id),
                "line_id": refund.line_id,
                "refunded_quantity": refund.refunded_quantity,
                "refunded_amount": float(refund.refunded_amount_set.get('shop_money', {}).get('amount', 0))
            }
            for refund in order.refunds
        ],
        "transactions": [
            {
                "id": str(transaction.id),
                "gateway": transaction.gateway,
                "status": transaction.status,
                "amount": float(transaction.amount_set.get('shop_money', {}).get('amount', 0)),
                "processed_at": transaction.processed_at.isoformat() if transaction.processed_at else None,
                "fees": [
                    {
                        "id": str(fee.id),
                        "amount": float(fee.fee_amount_set.get('shop_money', {}).get('amount', 0)),
                        "currency": fee.currency,
                        "estimated": fee.estimated
                    }
                    for fee in transaction.fees
                ]
            }
            for transaction in order.transactions
        ],
        "profit_breakdown": {
            "net_revenue": float(profit_data['net_revenue']),
            "cogs": float(profit_data['cogs']),
            "fees": float(profit_data['fees']),
            "shipping_cost": float(profit_data['shipping_cost']),
            "ad_spend": float(profit_data['ad_spend']),
            "net_profit": float(profit_data['net_profit']),
            "margin_pct": float(profit_data['margin_pct'])
        },
        "flags": profit_data['flags']
    }


@router.get("/health")
async def get_data_health(
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Get data health metrics."""
    # Calculate health score for last 30 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    health_score = await _calculate_data_health_score(db, shop, {
        'start': start_date,
        'end': end_date
    })
    
    # Get additional health metrics
    total_orders = await _get_total_orders(db, shop, start_date, end_date)
    orders_with_estimated_fees = await _get_orders_with_estimated_fees(db, shop, start_date, end_date)
    orders_missing_costs = await _get_orders_missing_costs(db, shop, start_date, end_date)
    
    return {
        "total_orders": total_orders,
        "orders_with_estimated_fees": orders_with_estimated_fees,
        "orders_missing_unit_costs": orders_missing_costs,
        "data_completeness_score": health_score,
        "last_updated": datetime.utcnow().isoformat(),
        "recommendations": _get_health_recommendations(health_score, orders_with_estimated_fees, orders_missing_costs)
    }


async def _calculate_data_health_score(
    db: AsyncSession, 
    shop: Shop, 
    date_range: dict
) -> float:
    """Calculate data health score (0-1)."""
    # This is a simplified calculation
    # In practice, you'd want more sophisticated health metrics
    return 0.85  # Placeholder


async def _get_total_orders(
    db: AsyncSession, 
    shop: Shop, 
    start_date: datetime, 
    end_date: datetime
) -> int:
    """Get total orders in date range."""
    result = await db.execute(
        select(func.count(Order.id))
        .where(
            and_(
                Order.shop_id == shop.id,
                Order.processed_at >= start_date,
                Order.processed_at <= end_date
            )
        )
    )
    return result.scalar() or 0


async def _get_orders_with_estimated_fees(
    db: AsyncSession, 
    shop: Shop, 
    start_date: datetime, 
    end_date: datetime
) -> int:
    """Get count of orders with estimated fees."""
    # This would need to be implemented based on your fee estimation logic
    return 0


async def _get_orders_missing_costs(
    db: AsyncSession, 
    shop: Shop, 
    start_date: datetime, 
    end_date: datetime
) -> int:
    """Get count of orders missing unit costs."""
    # This would need to be implemented based on your cost tracking logic
    return 0


def _get_health_recommendations(
    health_score: float, 
    estimated_fees: int, 
    missing_costs: int
) -> list:
    """Get health improvement recommendations."""
    recommendations = []
    
    if health_score < 0.8:
        recommendations.append("Data completeness is below 80%. Consider importing missing cost data.")
    
    if estimated_fees > 0:
        recommendations.append(f"{estimated_fees} orders have estimated fees. Verify fee settings.")
    
    if missing_costs > 0:
        recommendations.append(f"{missing_costs} orders are missing unit costs. Import cost data via CSV.")
    
    return recommendations
