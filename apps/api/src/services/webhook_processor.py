"""Webhook processing service."""

from typing import Dict, Any, List
from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db.models import (
    Order, OrderLine, RefundLine, Transaction, TransactionFee,
    InventoryItemCostSnapshot, DailyRollup
)
from ..services.profit_calculator import ProfitCalculator
from ..services.shopify_client import ShopifyClient
from ..utils.currency import normalize_amount, convert_currency
from ..utils.dedup import generate_dedup_key

profit_calculator = ProfitCalculator()


class WebhookProcessor:
    """Processes webhook events and updates database."""
    
    def __init__(self):
        self.shopify_client = ShopifyClient()
    
    async def process_order_create(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        payload: Dict[str, Any]
    ) -> None:
        """Process order creation webhook."""
        order_data = self._extract_order_data(payload)
        
        # Check if order already exists
        result = await db.execute(
            select(Order).where(
                Order.shop_id == shop.id,
                Order.shop_order_id == str(order_data['id'])
            )
        )
        existing_order = result.scalar_one_or_none()
        
        if existing_order:
            # Update existing order
            await self._update_order(db, existing_order, order_data)
        else:
            # Create new order
            await self._create_order(db, shop, order_data)
    
    async def process_order_update(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        payload: Dict[str, Any]
    ) -> None:
        """Process order update webhook."""
        await self.process_order_create(db, shop, payload)
    
    async def process_order_paid(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        payload: Dict[str, Any]
    ) -> None:
        """Process order paid webhook."""
        await self.process_order_create(db, shop, payload)
    
    async def process_order_cancelled(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        payload: Dict[str, Any]
    ) -> None:
        """Process order cancelled webhook."""
        await self.process_order_create(db, shop, payload)
    
    async def process_order_fulfilled(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        payload: Dict[str, Any]
    ) -> None:
        """Process order fulfilled webhook."""
        await self.process_order_create(db, shop, payload)
    
    async def process_order_partially_fulfilled(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        payload: Dict[str, Any]
    ) -> None:
        """Process order partially fulfilled webhook."""
        await self.process_order_create(db, shop, payload)
    
    async def process_refund_create(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        payload: Dict[str, Any]
    ) -> None:
        """Process refund creation webhook."""
        refund_data = self._extract_refund_data(payload)
        
        # Get the order
        result = await db.execute(
            select(Order).where(
                Order.shop_id == shop.id,
                Order.shop_order_id == str(refund_data['order_id'])
            )
        )
        order = result.scalar_one_or_none()
        
        if not order:
            return
        
        # Process refund lines
        for refund_line in refund_data.get('refund_line_items', []):
            await self._create_refund_line(db, shop, order, refund_line)
        
        # Recalculate order profit
        await self._recalculate_order_profit(db, order)
    
    async def process_transaction_create(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        payload: Dict[str, Any]
    ) -> None:
        """Process transaction creation webhook."""
        transaction_data = self._extract_transaction_data(payload)
        
        # Get the order
        result = await db.execute(
            select(Order).where(
                Order.shop_id == shop.id,
                Order.shop_order_id == str(transaction_data['order_id'])
            )
        )
        order = result.scalar_one_or_none()
        
        if not order:
            return
        
        # Create transaction
        await self._create_transaction(db, shop, order, transaction_data)
        
        # Recalculate order profit
        await self._recalculate_order_profit(db, order)
    
    def _extract_order_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extract order data from webhook payload."""
        return {
            'id': payload['id'],
            'order_number': payload.get('order_number'),
            'created_at': payload['created_at'],
            'updated_at': payload['updated_at'],
            'processed_at': payload.get('processed_at'),
            'currency': payload['currency'],
            'presentment_currency': payload.get('presentment_currency', payload['currency']),
            'total_price': payload['total_price'],
            'total_discounts': payload.get('total_discounts', '0'),
            'total_tax': payload.get('total_tax', '0'),
            'total_duties': payload.get('total_duties'),
            'total_shipping_price_set': payload.get('total_shipping_price_set'),
            'financial_status': payload['financial_status'],
            'fulfillment_status': payload.get('fulfillment_status'),
            'customer_id': payload.get('customer', {}).get('id') if payload.get('customer') else None,
            'line_items': payload.get('line_items', []),
            'refunds': payload.get('refunds', []),
            'transactions': payload.get('transactions', []),
        }
    
    def _extract_refund_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extract refund data from webhook payload."""
        return {
            'id': payload['id'],
            'order_id': payload['order_id'],
            'created_at': payload['created_at'],
            'refund_line_items': payload.get('refund_line_items', []),
        }
    
    def _extract_transaction_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extract transaction data from webhook payload."""
        return {
            'id': payload['id'],
            'order_id': payload['order_id'],
            'gateway': payload['gateway'],
            'status': payload['status'],
            'amount': payload['amount'],
            'currency': payload['currency'],
            'processed_at': payload.get('processed_at'),
            'fee': payload.get('fee'),
        }
    
    async def _create_order(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        order_data: Dict[str, Any]
    ) -> Order:
        """Create new order in database."""
        # Parse dates
        created_at = datetime.fromisoformat(order_data['created_at'].replace('Z', '+00:00'))
        processed_at = datetime.fromisoformat(
            order_data.get('processed_at', order_data['created_at']).replace('Z', '+00:00')
        )
        
        # Create order
        order = Order(
            shop_id=shop.id,
            shop_order_id=str(order_data['id']),
            created_at=created_at,
            processed_at=processed_at,
            currency=order_data['currency'],
            presentment_currency=order_data['presentment_currency'],
            current_total_price=Decimal(order_data['total_price']),
            current_total_discounts=Decimal(order_data['total_discounts']),
            current_total_tax=Decimal(order_data['total_tax']),
            current_total_duties=Decimal(order_data['total_duties']) if order_data.get('total_duties') else None,
            current_total_shipping_price_set=order_data.get('total_shipping_price_set'),
            financial_status=order_data['financial_status'],
            fulfillment_status=order_data.get('fulfillment_status'),
            customer_id=str(order_data['customer_id']) if order_data.get('customer_id') else None,
            flags={}
        )
        
        db.add(order)
        await db.commit()
        await db.refresh(order)
        
        # Process line items
        for line_item in order_data.get('line_items', []):
            await self._create_order_line(db, shop, order, line_item)
        
        # Process refunds
        for refund in order_data.get('refunds', []):
            for refund_line in refund.get('refund_line_items', []):
                await self._create_refund_line(db, shop, order, refund_line)
        
        # Process transactions
        for transaction in order_data.get('transactions', []):
            await self._create_transaction(db, shop, order, transaction)
        
        # Calculate profit
        await self._recalculate_order_profit(db, order)
        
        return order
    
    async def _update_order(
        self, 
        db: AsyncSession, 
        order: Order, 
        order_data: Dict[str, Any]
    ) -> None:
        """Update existing order."""
        # Update order fields
        order.updated_at = datetime.utcnow()
        order.current_total_price = Decimal(order_data['total_price'])
        order.current_total_discounts = Decimal(order_data['total_discounts'])
        order.current_total_tax = Decimal(order_data['total_tax'])
        order.current_total_duties = Decimal(order_data['total_duties']) if order_data.get('total_duties') else None
        order.financial_status = order_data['financial_status']
        order.fulfillment_status = order_data.get('fulfillment_status')
        
        await db.commit()
        
        # Recalculate profit
        await self._recalculate_order_profit(db, order)
    
    async def _create_order_line(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        order: Order, 
        line_item: Dict[str, Any]
    ) -> OrderLine:
        """Create order line item."""
        # Get unit cost from inventory item
        unit_cost, cost_source = await self._get_unit_cost(
            db, shop, line_item['inventory_item_id'], order.created_at
        )
        
        order_line = OrderLine(
            shop_id=shop.id,
            order_id=order.id,
            line_id=str(line_item['id']),
            product_id=str(line_item['product_id']),
            variant_id=str(line_item['variant_id']),
            inventory_item_id=str(line_item['inventory_item_id']),
            quantity=line_item['quantity'],
            price_set=line_item['price_set'],
            discount_allocations=line_item.get('discount_allocations', []),
            presentment_currency=order.presentment_currency,
            shop_currency=order.currency,
            effective_unit_cost=unit_cost,
            cost_source=cost_source
        )
        
        db.add(order_line)
        await db.commit()
        await db.refresh(order_line)
        
        return order_line
    
    async def _create_refund_line(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        order: Order, 
        refund_line: Dict[str, Any]
    ) -> RefundLine:
        """Create refund line item."""
        refund_line_obj = RefundLine(
            shop_id=shop.id,
            order_id=order.id,
            line_id=str(refund_line['line_item_id']),
            refunded_quantity=refund_line['quantity'],
            refunded_amount_set=refund_line.get('subtotal_set', {})
        )
        
        db.add(refund_line_obj)
        await db.commit()
        await db.refresh(refund_line_obj)
        
        return refund_line_obj
    
    async def _create_transaction(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        order: Order, 
        transaction_data: Dict[str, Any]
    ) -> Transaction:
        """Create transaction."""
        processed_at = None
        if transaction_data.get('processed_at'):
            processed_at = datetime.fromisoformat(
                transaction_data['processed_at'].replace('Z', '+00:00')
            )
        
        transaction = Transaction(
            shop_id=shop.id,
            order_id=order.id,
            gateway=transaction_data['gateway'],
            status=transaction_data['status'],
            amount_set={
                'shop_money': {
                    'amount': transaction_data['amount'],
                    'currency_code': transaction_data['currency']
                },
                'presentment_money': {
                    'amount': transaction_data['amount'],
                    'currency_code': transaction_data['currency']
                }
            },
            processed_at=processed_at
        )
        
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        
        # Create transaction fee if available
        if transaction_data.get('fee'):
            await self._create_transaction_fee(db, shop, transaction, transaction_data)
        
        return transaction
    
    async def _create_transaction_fee(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        transaction: Transaction, 
        transaction_data: Dict[str, Any]
    ) -> TransactionFee:
        """Create transaction fee."""
        fee_amount = transaction_data.get('fee', '0')
        
        transaction_fee = TransactionFee(
            shop_id=shop.id,
            transaction_id=transaction.id,
            fee_amount_set={
                'shop_money': {
                    'amount': fee_amount,
                    'currency_code': transaction_data['currency']
                },
                'presentment_money': {
                    'amount': fee_amount,
                    'currency_code': transaction_data['currency']
                }
            },
            currency=transaction_data['currency'],
            presentment_currency=transaction_data['currency'],
            estimated=False
        )
        
        db.add(transaction_fee)
        await db.commit()
        await db.refresh(transaction_fee)
        
        return transaction_fee
    
    async def _get_unit_cost(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        inventory_item_id: str, 
        order_date: datetime
    ) -> tuple[Decimal | None, str]:
        """Get unit cost for inventory item at order date."""
        # Look for existing snapshot
        result = await db.execute(
            select(InventoryItemCostSnapshot)
            .where(
                InventoryItemCostSnapshot.shop_id == shop.id,
                InventoryItemCostSnapshot.inventory_item_id == inventory_item_id,
                InventoryItemCostSnapshot.effective_date <= order_date
            )
            .order_by(InventoryItemCostSnapshot.effective_date.desc())
        )
        snapshot = result.scalar_one_or_none()
        
        if snapshot:
            return snapshot.unit_cost, snapshot.source
        
        # Try to fetch from Shopify API
        try:
            unit_cost = await self.shopify_client.get_inventory_item_cost(
                shop, inventory_item_id
            )
            if unit_cost:
                # Store snapshot
                snapshot = InventoryItemCostSnapshot(
                    shop_id=shop.id,
                    inventory_item_id=inventory_item_id,
                    effective_date=order_date,
                    unit_cost=unit_cost,
                    currency=shop.currency,
                    source='api'
                )
                db.add(snapshot)
                await db.commit()
                
                return unit_cost, 'api'
        except Exception:
            pass
        
        return None, 'null'
    
    async def _recalculate_order_profit(
        self, 
        db: AsyncSession, 
        order: Order
    ) -> None:
        """Recalculate order profit and update rollups."""
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
        
        # Calculate profit
        profit_data = await profit_calculator.calculate_order_profit(
            db, order_with_data
        )
        
        # Update order flags
        order.flags = profit_data['flags']
        await db.commit()
        
        # Update daily rollup
        await self._update_daily_rollup(db, order, profit_data)
    
    async def _update_daily_rollup(
        self, 
        db: AsyncSession, 
        order: Order, 
        profit_data: Dict[str, Any]
    ) -> None:
        """Update daily rollup for order's date."""
        order_date = order.processed_at.date()
        
        # Get or create daily rollup
        result = await db.execute(
            select(DailyRollup).where(
                DailyRollup.shop_id == order.shop_id,
                DailyRollup.date == order_date
            )
        )
        rollup = result.scalar_one_or_none()
        
        if not rollup:
            rollup = DailyRollup(
                shop_id=order.shop_id,
                date=order_date,
                net_revenue=Decimal('0'),
                cogs=Decimal('0'),
                fees=Decimal('0'),
                shipping_cost=Decimal('0'),
                ad_spend={},
                net_profit=Decimal('0'),
                margin_pct=Decimal('0')
            )
            db.add(rollup)
        
        # Recalculate daily totals (this would need to aggregate all orders for the day)
        # For now, just update this order's contribution
        rollup.net_revenue += profit_data['net_revenue']
        rollup.cogs += profit_data['cogs']
        rollup.fees += profit_data['fees']
        rollup.shipping_cost += profit_data['shipping_cost']
        rollup.net_profit += profit_data['net_profit']
        
        if rollup.net_revenue > 0:
            rollup.margin_pct = (rollup.net_profit / rollup.net_revenue) * 100
        
        await db.commit()
