"""Authentication middleware and dependencies."""

from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt

from ..config.settings import get_settings
from ..db.models import Shop
from ..db.database import get_db

settings = get_settings()
security = HTTPBearer()


async def get_current_shop(
    request: Request,
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Shop:
    """Get current shop from JWT token."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        shop_id: str = payload.get("sub")
        if shop_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get shop from database
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    
    if shop is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Shop not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return shop


async def get_shop_from_request(request: Request) -> Optional[str]:
    """Extract shop domain from request headers or query params."""
    # Check for shop domain in headers
    shop_domain = request.headers.get("X-Shopify-Shop-Domain")
    if shop_domain:
        return shop_domain
    
    # Check for shop domain in query params
    shop_domain = request.query_params.get("shop")
    if shop_domain:
        return shop_domain
    
    return None


def create_access_token(shop_id: str) -> str:
    """Create JWT access token for shop."""
    from datetime import datetime, timedelta
    
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode = {"sub": str(shop_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt
