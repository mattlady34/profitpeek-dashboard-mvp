"""Profit calculation service."""

from typing import Dict, Any, List
from decimal import Decimal
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..db.models import Order, OrderLine, RefundLine, Transaction, TransactionFee, Settings
from ..config.settings import get_settings

settings = get_settings()


class ProfitCalculator:
    """Calculates profit metrics for orders and periods."""
    
    async def calculate_order_profit(
        self, 
        db: AsyncSession, 
        order: Order
    ) -> Dict[str, Any]:
        """Calculate profit breakdown for a single order."""
        # Get order with all related data
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.lines),
                selectinload(Order.refunds),
                selectinload(Order.transactions).selectinload(Transaction.fees)
            )
            .where(Order.id == order.id)
        )
        order_with_data = result.scalar_one()
        
        # Calculate components
        net_revenue = self._calculate_net_revenue(order_with_data)
        cogs = await self._calculate_cogs(db, order_with_data)
        fees = await self._calculate_fees(db, order_with_data)
        shipping_cost = await self._calculate_shipping_cost(db, order_with_data)
        ad_spend = await self._calculate_ad_spend(db, order_with_data)
        
        # Calculate totals
        net_profit = net_revenue - cogs - fees - shipping_cost - ad_spend
        margin_pct = (net_profit / net_revenue * 100) if net_revenue > 0 else Decimal('0')
        
        # Determine flags
        flags = self._calculate_flags(order_with_data, fees, cogs)
        
        return {
            'net_revenue': net_revenue,
            'cogs': cogs,
            'fees': fees,
            'shipping_cost': shipping_cost,
            'ad_spend': ad_spend,
            'net_profit': net_profit,
            'margin_pct': margin_pct,
            'flags': flags
        }
    
    def _calculate_net_revenue(self, order: Order) -> Decimal:
        """Calculate net revenue (total - refunds)."""
        total_revenue = order.current_total_price
        
        # Subtract refunds
        refunded_amount = Decimal('0')
        for refund in order.refunds:
            refunded_amount += self._extract_amount_from_price_set(
                refund.refunded_amount_set, order.currency
            )
        
        return total_revenue - refunded_amount
    
    async def _calculate_cogs(
        self, 
        db: AsyncSession, 
        order: Order
    ) -> Decimal:
        """Calculate cost of goods sold."""
        total_cogs = Decimal('0')
        
        for line in order.lines:
            if line.effective_unit_cost:
                line_cogs = line.effective_unit_cost * line.quantity
                
                # Adjust for refunds
                refunded_qty = self._get_refunded_quantity(order, line.line_id)
                if refunded_qty > 0:
                    refunded_cogs = line.effective_unit_cost * refunded_qty
                    line_cogs -= refunded_cogs
                
                total_cogs += line_cogs
        
        return total_cogs
    
    async def _calculate_fees(
        self, 
        db: AsyncSession, 
        order: Order
    ) -> Decimal:
        """Calculate processing fees."""
        total_fees = Decimal('0')
        estimated_fees = False
        
        # Sum actual transaction fees
        for transaction in order.transactions:
            for fee in transaction.fees:
                fee_amount = self._extract_amount_from_price_set(
                    fee.fee_amount_set, order.currency
                )
                total_fees += fee_amount
                
                if fee.estimated:
                    estimated_fees = True
        
        # If no fees found, estimate using settings
        if total_fees == 0:
            total_fees = await self._estimate_fees(db, order)
            estimated_fees = True
        
        return total_fees
    
    async def _calculate_shipping_cost(
        self, 
        db: AsyncSession, 
        order: Order
    ) -> Decimal:
        """Calculate shipping cost using settings."""
        # Get shop settings
        result = await db.execute(
            select(Settings).where(Settings.shop_id == order.shop_id)
        )
        settings_obj = result.scalar_one_or_none()
        
        if not settings_obj:
            return Decimal('0')
        
        shipping_rule = settings_obj.shipping_cost_rule
        
        if shipping_rule['type'] == 'flat':
            return Decimal(str(shipping_rule['value']))
        elif shipping_rule['type'] == 'percentage':
            percentage = Decimal(str(shipping_rule['value'])) / 100
            return order.current_total_price * percentage
        
        return Decimal('0')
    
    async def _calculate_ad_spend(
        self, 
        db: AsyncSession, 
        order: Order
    ) -> Decimal:
        """Calculate ad spend for order date."""
        # This would typically be calculated at the daily level
        # For individual orders, we might allocate based on order value
        # For now, return 0 as ad spend is tracked daily
        return Decimal('0')
    
    def _calculate_flags(
        self, 
        order: Order, 
        fees: Decimal, 
        cogs: Decimal
    ) -> Dict[str, Any]:
        """Calculate order flags."""
        flags = {}
        
        # Check for estimated fees
        has_estimated_fees = False
        for transaction in order.transactions:
            for fee in transaction.fees:
                if fee.estimated:
                    has_estimated_fees = True
                    break
        
        if has_estimated_fees or fees == 0:
            flags['fees_estimated'] = True
        
        # Check for missing unit costs
        has_missing_costs = False
        for line in order.lines:
            if not line.effective_unit_cost:
                has_missing_costs = True
                break
        
        if has_missing_costs:
            flags['no_unit_cost'] = True
        
        # Check for multi-currency
        if order.currency != order.presentment_currency:
            flags['multi_currency'] = True
        
        # Check for refunds
        if order.refunds:
            flags['has_refunds'] = True
        
        return flags
    
    def _extract_amount_from_price_set(
        self, 
        price_set: Dict[str, Any], 
        currency: str
    ) -> Decimal:
        """Extract amount from price set for given currency."""
        if not price_set:
            return Decimal('0')
        
        # Try shop money first
        if 'shop_money' in price_set:
            shop_money = price_set['shop_money']
            if shop_money.get('currency_code') == currency:
                return Decimal(shop_money.get('amount', '0'))
        
        # Try presentment money
        if 'presentment_money' in price_set:
            presentment_money = price_set['presentment_money']
            if presentment_money.get('currency_code') == currency:
                return Decimal(presentment_money.get('amount', '0'))
        
        # Fallback to first available amount
        for money_type in ['shop_money', 'presentment_money']:
            if money_type in price_set:
                money = price_set[money_type]
                return Decimal(money.get('amount', '0'))
        
        return Decimal('0')
    
    def _get_refunded_quantity(self, order: Order, line_id: str) -> int:
        """Get refunded quantity for a line item."""
        total_refunded = 0
        for refund in order.refunds:
            if refund.line_id == line_id:
                total_refunded += refund.refunded_quantity
        return total_refunded
    
    async def _estimate_fees(
        self, 
        db: AsyncSession, 
        order: Order
    ) -> Decimal:
        """Estimate processing fees using settings."""
        # Get shop settings
        result = await db.execute(
            select(Settings).where(Settings.shop_id == order.shop_id)
        )
        settings_obj = result.scalar_one_or_none()
        
        if not settings_obj:
            # Use default settings
            percentage = Decimal(str(settings.default_fee_percentage)) / 100
            fixed_fee = Decimal(str(settings.default_fee_fixed))
            return (order.current_total_price * percentage) + fixed_fee
        
        # Use shop-specific settings
        percentage = Decimal(str(settings_obj.fee_default_pct)) / 100
        fixed_fee = Decimal('0.30')  # Default fixed fee
        
        return (order.current_total_price * percentage) + fixed_fee
    
    async def calculate_period_profit(
        self, 
        db: AsyncSession, 
        shop_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """Calculate profit for a time period."""
        # This would aggregate all orders in the period
        # For now, return a placeholder structure
        return {
            'net_revenue': Decimal('0'),
            'cogs': Decimal('0'),
            'fees': Decimal('0'),
            'shipping_cost': Decimal('0'),
            'ad_spend': Decimal('0'),
            'net_profit': Decimal('0'),
            'margin_pct': Decimal('0'),
            'orders_count': 0,
            'aov': Decimal('0')
        }
