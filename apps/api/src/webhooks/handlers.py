"""Webhook handlers for Shopify events."""

import json
import hashlib
import hmac
from typing import Dict, Any
from datetime import datetime

from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..config.settings import get_settings
from ..db.models import Shop, WebhookEvent
from ..db.database import get_db
from ..services.webhook_processor import WebhookProcessor
from ..services.profit_calculator import ProfitCalculator

settings = get_settings()


class WebhookHandler:
    """Handles incoming Shopify webhooks."""
    
    def __init__(self):
        self.processor = WebhookProcessor()
        self.calculator = ProfitCalculator()
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature from Shopify."""
        calculated_signature = hmac.new(
            settings.shopify_webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={calculated_signature}", signature)
    
    async def handle_webhook(
        self,
        request: Request,
        topic: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Handle incoming webhook."""
        # Get raw body
        body = await request.body()
        
        # Verify signature
        signature = request.headers.get("X-Shopify-Hmac-Sha256")
        if not signature or not self.verify_webhook_signature(body, signature):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        # Get shop domain
        shop_domain = request.headers.get("X-Shopify-Shop-Domain")
        if not shop_domain:
            raise HTTPException(status_code=400, detail="Missing shop domain")
        
        # Get shop from database
        result = await db.execute(
            select(Shop).where(Shop.shop_domain == shop_domain)
        )
        shop = result.scalar_one_or_none()
        
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        # Parse payload
        try:
            payload = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
        # Create webhook event record
        webhook_event = await self._create_webhook_event(
            db, shop, topic, payload
        )
        
        # Process webhook based on topic
        try:
            await self._process_webhook_by_topic(db, shop, topic, payload)
            webhook_event.status = "completed"
            webhook_event.processed_at = datetime.utcnow()
        except Exception as e:
            webhook_event.status = "failed"
            webhook_event.error = str(e)
            raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")
        finally:
            await db.commit()
        
        return {"status": "success", "webhook_id": str(webhook_event.id)}
    
    async def _create_webhook_event(
        self,
        db: AsyncSession,
        shop: Shop,
        topic: str,
        payload: Dict[str, Any]
    ) -> WebhookEvent:
        """Create webhook event record."""
        # Generate dedup key
        resource_id = str(payload.get('id', ''))
        timestamp = payload.get('created_at', datetime.utcnow().isoformat())
        dedup_key = f"{topic}:{shop.shop_domain}:{resource_id}:{timestamp}"
        
        # Check for duplicate
        result = await db.execute(
            select(WebhookEvent).where(WebhookEvent.dedup_key == dedup_key)
        )
        existing_event = result.scalar_one_or_none()
        
        if existing_event:
            return existing_event
        
        # Create new event
        webhook_event = WebhookEvent(
            shop_id=shop.id,
            topic=topic,
            shop_resource_id=resource_id,
            dedup_key=dedup_key,
            status="pending"
        )
        
        db.add(webhook_event)
        await db.commit()
        await db.refresh(webhook_event)
        
        return webhook_event
    
    async def _process_webhook_by_topic(
        self,
        db: AsyncSession,
        shop: Shop,
        topic: str,
        payload: Dict[str, Any]
    ) -> None:
        """Process webhook based on topic."""
        if topic == "orders/create":
            await self.processor.process_order_create(db, shop, payload)
        elif topic == "orders/updated":
            await self.processor.process_order_update(db, shop, payload)
        elif topic == "orders/paid":
            await self.processor.process_order_paid(db, shop, payload)
        elif topic == "orders/cancelled":
            await self.processor.process_order_cancelled(db, shop, payload)
        elif topic == "orders/fulfilled":
            await self.processor.process_order_fulfilled(db, shop, payload)
        elif topic == "orders/partially_fulfilled":
            await self.processor.process_order_partially_fulfilled(db, shop, payload)
        elif topic == "refunds/create":
            await self.processor.process_refund_create(db, shop, payload)
        elif topic == "transactions/create":
            await self.processor.process_transaction_create(db, shop, payload)
        else:
            raise ValueError(f"Unknown webhook topic: {topic}")


# Global instance
webhook_handler = WebhookHandler()
