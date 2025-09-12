"""Backfill API routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..auth.middleware import get_current_shop
from ..db.models import Shop
from ..services.backfill_service import backfill_service

router = APIRouter(prefix="/backfill", tags=["backfill"])


@router.post("/start")
async def start_backfill(
    days: int = Query(90, description="Number of days to backfill", ge=1, le=365),
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Start backfill process for the shop."""
    result = await backfill_service.start_backfill(db, shop, days)
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result


@router.get("/status/{operation_id}")
async def get_backfill_status(
    operation_id: str,
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Get status of backfill operation."""
    result = await backfill_service.check_backfill_status(db, shop, operation_id)
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result


@router.post("/resume/{operation_id}")
async def resume_backfill(
    operation_id: str,
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Resume a backfill operation."""
    result = await backfill_service.resume_backfill(db, shop, operation_id)
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result


@router.post("/cancel/{operation_id}")
async def cancel_backfill(
    operation_id: str,
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Cancel a backfill operation."""
    result = await backfill_service.cancel_backfill(db, shop, operation_id)
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result


@router.get("/history")
async def get_backfill_history(
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Get backfill history for the shop."""
    history = await backfill_service.get_backfill_history(db, shop)
    return {"history": history}


@router.get("/estimate")
async def estimate_backfill_time(
    days: int = Query(90, description="Number of days to backfill", ge=1, le=365),
    shop: Shop = Depends(get_current_shop),
    db: AsyncSession = Depends(get_db)
):
    """Estimate time required for backfill."""
    result = await backfill_service.estimate_backfill_time(db, shop, days)
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result
