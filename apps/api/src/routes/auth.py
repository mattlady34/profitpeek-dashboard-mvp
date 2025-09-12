"""Authentication routes for Shopify OAuth."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..auth.shopify import shopify_auth
from ..auth.middleware import create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/start")
async def start_auth(
    shop: str = Query(..., description="Shop domain (e.g., mystore.myshopify.com)"),
    db: AsyncSession = Depends(get_db)
):
    """Start Shopify OAuth flow."""
    if not shop:
        raise HTTPException(status_code=400, detail="Shop parameter is required")
    
    # Generate authorization URL
    auth_url = shopify_auth.generate_auth_url(shop)
    
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def auth_callback(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Shopify OAuth callback."""
    query_params = dict(request.query_params)
    
    # Verify HMAC signature
    if not shopify_auth.verify_hmac(query_params):
        raise HTTPException(status_code=400, detail="Invalid HMAC signature")
    
    # Check for errors
    if 'error' in query_params:
        error_description = query_params.get('error_description', 'Unknown error')
        raise HTTPException(status_code=400, detail=f"OAuth error: {error_description}")
    
    # Get authorization code
    code = query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    
    # Get shop domain
    shop_domain = query_params.get('shop')
    if not shop_domain:
        raise HTTPException(status_code=400, detail="Shop domain not provided")
    
    try:
        # Exchange code for access token
        token_data = await shopify_auth.exchange_code_for_token(
            shop_domain, code, db
        )
        
        # Create JWT token for the shop
        shop = await shopify_auth.get_shop_by_domain(db, shop_domain)
        if not shop:
            raise HTTPException(status_code=500, detail="Failed to retrieve shop data")
        
        access_token = create_access_token(str(shop.id))
        
        # Redirect to frontend with token
        frontend_url = f"http://localhost:3000/dashboard?token={access_token}"
        return RedirectResponse(url=frontend_url)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@router.get("/status")
async def auth_status(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Check authentication status."""
    shop_domain = request.headers.get("X-Shopify-Shop-Domain")
    if not shop_domain:
        return {"authenticated": False, "message": "No shop domain provided"}
    
    shop = await shopify_auth.get_shop_by_domain(db, shop_domain)
    if not shop:
        return {"authenticated": False, "message": "Shop not found"}
    
    return {
        "authenticated": True,
        "shop": {
            "domain": shop.shop_domain,
            "currency": shop.currency,
            "plan": shop.plan,
            "scopes": shop.scopes
        }
    }