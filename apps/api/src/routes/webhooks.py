"""Webhook routes for Shopify events."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..webhooks.handlers import webhook_handler

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/orders_create")
async def orders_create(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle orders/create webhook."""
    return await webhook_handler.handle_webhook(request, "orders/create", db)


@router.post("/orders_updated")
async def orders_updated(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle orders/updated webhook."""
    return await webhook_handler.handle_webhook(request, "orders/updated", db)


@router.post("/orders_paid")
async def orders_paid(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle orders/paid webhook."""
    return await webhook_handler.handle_webhook(request, "orders/paid", db)


@router.post("/orders_cancelled")
async def orders_cancelled(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle orders/cancelled webhook."""
    return await webhook_handler.handle_webhook(request, "orders/cancelled", db)


@router.post("/orders_fulfilled")
async def orders_fulfilled(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle orders/fulfilled webhook."""
    return await webhook_handler.handle_webhook(request, "orders/fulfilled", db)


@router.post("/orders_partially_fulfilled")
async def orders_partially_fulfilled(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle orders/partially_fulfilled webhook."""
    return await webhook_handler.handle_webhook(request, "orders/partially_fulfilled", db)


@router.post("/refunds_create")
async def refunds_create(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle refunds/create webhook."""
    return await webhook_handler.handle_webhook(request, "refunds/create", db)


@router.post("/transactions_create")
async def transactions_create(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle transactions/create webhook."""
    return await webhook_handler.handle_webhook(request, "transactions/create", db)
