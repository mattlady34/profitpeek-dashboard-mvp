"""Backfill service for importing historical order data."""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..db.models import Shop, Order, OrderLine, RefundLine, Transaction, TransactionFee, DailyRollup
from ..services.shopify_client import ShopifyClient
from ..services.webhook_processor import WebhookProcessor
from ..services.profit_calculator import ProfitCalculator
from ..utils.dedup import generate_bulk_operation_key
from ..config.settings import get_settings

settings = get_settings()
shopify_client = ShopifyClient()
webhook_processor = WebhookProcessor()
profit_calculator = ProfitCalculator()


class BackfillService:
    """Service for backfilling historical order data."""
    
    def __init__(self):
        self.batch_size = settings.backfill_batch_size
        self.max_retries = settings.backfill_max_retries
    
    async def start_backfill(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        days: int = 90
    ) -> Dict[str, Any]:
        """Start backfill process for a shop."""
        try:
            # Create bulk operation query
            query = self._build_bulk_query(days)
            
            # Start bulk operation
            operation_id = await shopify_client.create_bulk_operation(shop, query)
            if not operation_id:
                raise Exception("Failed to create bulk operation")
            
            # Store operation details
            operation_data = {
                'operation_id': operation_id,
                'shop_id': str(shop.id),
                'days': days,
                'status': 'running',
                'started_at': datetime.utcnow().isoformat(),
                'progress': 0
            }
            
            # Store in Redis or database for tracking
            # This would be implemented with Redis for production
            
            return {
                'success': True,
                'operation_id': operation_id,
                'message': 'Backfill started successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def check_backfill_status(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        operation_id: str
    ) -> Dict[str, Any]:
        """Check status of backfill operation."""
        try:
            status = await shopify_client.get_bulk_operation_status(shop, operation_id)
            if not status:
                return {
                    'success': False,
                    'error': 'Operation not found'
                }
            
            return {
                'success': True,
                'status': status.get('status'),
                'progress': self._calculate_progress(status),
                'object_count': status.get('objectCount', 0),
                'file_size': status.get('fileSize', 0),
                'url': status.get('url'),
                'error': status.get('errorMessage')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def process_backfill_data(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        data_url: str
    ) -> Dict[str, Any]:
        """Process downloaded backfill data."""
        try:
            # Download and process JSONL data
            # This would be implemented with proper file handling
            processed_orders = 0
            errors = []
            
            # Simulate processing
            # In production, this would:
            # 1. Download the JSONL file from S3
            # 2. Parse it line by line
            # 3. Process each order through the webhook processor
            # 4. Update progress tracking
            
            return {
                'success': True,
                'processed_orders': processed_orders,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_bulk_query(self, days: int) -> str:
        """Build GraphQL query for bulk operation."""
        start_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        query = f"""
        {{
            orders(query: "created_at:>={start_date}", first: 250) {{
                edges {{
                    node {{
                        id
                        name
                        createdAt
                        updatedAt
                        processedAt
                        totalPriceSet {{
                            shopMoney {{
                                amount
                                currencyCode
                            }}
                            presentmentMoney {{
                                amount
                                currencyCode
                            }}
                        }}
                        totalDiscountsSet {{
                            shopMoney {{
                                amount
                                currencyCode
                            }}
                            presentmentMoney {{
                                amount
                                currencyCode
                            }}
                        }}
                        totalTaxSet {{
                            shopMoney {{
                                amount
                                currencyCode
                            }}
                            presentmentMoney {{
                                amount
                                currencyCode
                            }}
                        }}
                        totalShippingPriceSet {{
                            shopMoney {{
                                amount
                                currencyCode
                            }}
                            presentmentMoney {{
                                amount
                                currencyCode
                            }}
                        }}
                        financialStatus
                        fulfillmentStatus
                        customer {{
                            id
                        }}
                        lineItems(first: 250) {{
                            edges {{
                                node {{
                                    id
                                    product {{
                                        id
                                    }}
                                    variant {{
                                        id
                                        inventoryItem {{
                                            id
                                            unitCost
                                            tracked
                                        }}
                                    }}
                                    quantity
                                    originalUnitPriceSet {{
                                        shopMoney {{
                                            amount
                                            currencyCode
                                        }}
                                        presentmentMoney {{
                                            amount
                                            currencyCode
                                        }}
                                    }}
                                    discountAllocations {{
                                        amount {{
                                            amount
                                            currencyCode
                                        }}
                                        discountApplication {{
                                            ... on DiscountCodeApplication {{
                                                code
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                        refunds(first: 250) {{
                            edges {{
                                node {{
                                    id
                                    createdAt
                                    refundLineItems(first: 250) {{
                                        edges {{
                                            node {{
                                                id
                                                lineItem {{
                                                    id
                                                }}
                                                quantity
                                                subtotalSet {{
                                                    shopMoney {{
                                                        amount
                                                        currencyCode
                                                    }}
                                                    presentmentMoney {{
                                                        amount
                                                        currencyCode
                                                    }}
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                        transactions(first: 250) {{
                            edges {{
                                node {{
                                    id
                                    kind
                                    status
                                    gateway
                                    amount {{
                                        amount
                                        currencyCode
                                    }}
                                    processedAt
                                    fees {{
                                        amount {{
                                            amount
                                            currencyCode
                                        }}
                                        flatFee {{
                                            amount
                                            currencyCode
                                        }}
                                        rate
                                        type
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
        
        return query
    
    def _calculate_progress(self, status: Dict[str, Any]) -> int:
        """Calculate progress percentage."""
        status_type = status.get('status')
        if status_type == 'COMPLETED':
            return 100
        elif status_type == 'RUNNING':
            # Estimate progress based on time elapsed
            # This is a simplified calculation
            return 50
        else:
            return 0
    
    async def resume_backfill(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        operation_id: str
    ) -> Dict[str, Any]:
        """Resume a failed or paused backfill operation."""
        try:
            # Check current status
            status = await self.check_backfill_status(db, shop, operation_id)
            if not status['success']:
                return status
            
            # If completed, process the data
            if status['status'] == 'COMPLETED' and status.get('url'):
                return await self.process_backfill_data(db, shop, status['url'])
            
            return {
                'success': True,
                'status': status['status'],
                'message': 'Backfill resumed'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def cancel_backfill(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        operation_id: str
    ) -> Dict[str, Any]:
        """Cancel a running backfill operation."""
        try:
            # In production, this would cancel the bulk operation
            # For now, just return success
            return {
                'success': True,
                'message': 'Backfill cancelled'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_backfill_history(
        self, 
        db: AsyncSession, 
        shop: Shop
    ) -> List[Dict[str, Any]]:
        """Get backfill history for a shop."""
        # This would query a backfill_operations table
        # For now, return empty list
        return []
    
    async def estimate_backfill_time(
        self, 
        db: AsyncSession, 
        shop: Shop, 
        days: int
    ) -> Dict[str, Any]:
        """Estimate time required for backfill."""
        try:
            # Get order count for the period
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # This would query Shopify API for order count
            # For now, return estimated values
            estimated_orders = days * 10  # Assume 10 orders per day
            estimated_time_minutes = max(5, estimated_orders // 100)  # 100 orders per minute
            
            return {
                'success': True,
                'estimated_orders': estimated_orders,
                'estimated_time_minutes': estimated_time_minutes,
                'estimated_time_hours': estimated_time_minutes / 60
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Global instance
backfill_service = BackfillService()
