"""Shopify OAuth authentication."""

import hashlib
import hmac
import secrets
from urllib.parse import urlencode
from typing import Optional

import httpx
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..config.settings import get_settings
from ..db.models import Shop
from ..db.database import get_db

settings = get_settings()


class ShopifyAuth:
    """Shopify OAuth authentication handler."""
    
    def __init__(self):
        self.api_key = settings.shopify_api_key
        self.api_secret = settings.shopify_api_secret
        self.redirect_uri = settings.shopify_redirect_uri
        self.scopes = ",".join(settings.shopify_scopes)
    
    def generate_auth_url(self, shop_domain: str, state: Optional[str] = None) -> str:
        """Generate Shopify OAuth authorization URL."""
        if not shop_domain.endswith('.myshopify.com'):
            shop_domain = f"{shop_domain}.myshopify.com"
        
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            'client_id': self.api_key,
            'scope': self.scopes,
            'redirect_uri': self.redirect_uri,
            'state': state,
        }
        
        return f"https://{shop_domain}/admin/oauth/authorize?{urlencode(params)}"
    
    def verify_hmac(self, query_params: dict) -> bool:
        """Verify HMAC signature from Shopify callback."""
        hmac_param = query_params.get('hmac')
        if not hmac_param:
            return False
        
        # Remove hmac and signature from params
        params = {k: v for k, v in query_params.items() if k not in ['hmac', 'signature']}
        
        # Sort parameters and create query string
        sorted_params = sorted(params.items())
        query_string = urlencode(sorted_params)
        
        # Create HMAC
        calculated_hmac = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(calculated_hmac, hmac_param)
    
    async def exchange_code_for_token(
        self, 
        shop_domain: str, 
        code: str, 
        db: AsyncSession
    ) -> dict:
        """Exchange authorization code for access token."""
        if not shop_domain.endswith('.myshopify.com'):
            shop_domain = f"{shop_domain}.myshopify.com"
        
        url = f"https://{shop_domain}/admin/oauth/access_token"
        
        data = {
            'client_id': self.api_key,
            'client_secret': self.api_secret,
            'code': code,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            
            if 'access_token' not in token_data:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get access token from Shopify"
                )
            
            # Get shop information
            shop_info = await self._get_shop_info(shop_domain, token_data['access_token'])
            
            # Store shop and token in database
            await self._store_shop_data(db, shop_domain, token_data, shop_info)
            
            return {
                'access_token': token_data['access_token'],
                'shop_domain': shop_domain,
                'shop_info': shop_info
            }
    
    async def _get_shop_info(self, shop_domain: str, access_token: str) -> dict:
        """Get shop information from Shopify API."""
        url = f"https://{shop_domain}/admin/api/{settings.shopify_api_version}/shop.json"
        headers = {
            'X-Shopify-Access-Token': access_token,
            'Content-Type': 'application/json',
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return data['shop']
    
    async def _store_shop_data(
        self, 
        db: AsyncSession, 
        shop_domain: str, 
        token_data: dict, 
        shop_info: dict
    ) -> Shop:
        """Store shop data in database."""
        # Check if shop already exists
        result = await db.execute(
            select(Shop).where(Shop.shop_domain == shop_domain)
        )
        existing_shop = result.scalar_one_or_none()
        
        if existing_shop:
            # Update existing shop
            existing_shop.access_token = token_data['access_token']
            existing_shop.currency = shop_info.get('currency', 'USD')
            existing_shop.email = shop_info.get('email')
            existing_shop.plan = shop_info.get('plan_name')
            existing_shop.scopes = token_data.get('scope', '').split(',')
            existing_shop.updated_at = func.now()
            shop = existing_shop
        else:
            # Create new shop
            shop = Shop(
                shop_domain=shop_domain,
                access_token=token_data['access_token'],
                currency=shop_info.get('currency', 'USD'),
                email=shop_info.get('email'),
                plan=shop_info.get('plan_name'),
                scopes=token_data.get('scope', '').split(','),
                timezone=shop_info.get('timezone', 'UTC'),
            )
            db.add(shop)
        
        await db.commit()
        await db.refresh(shop)
        
        return shop
    
    async def get_shop_by_domain(self, db: AsyncSession, shop_domain: str) -> Optional[Shop]:
        """Get shop by domain."""
        result = await db.execute(
            select(Shop).where(Shop.shop_domain == shop_domain)
        )
        return result.scalar_one_or_none()
    
    async def refresh_access_token(self, db: AsyncSession, shop: Shop) -> bool:
        """Refresh access token if needed."""
        # For now, we'll just return True as Shopify tokens don't expire
        # In a real implementation, you might want to check token validity
        return True


# Global instance
shopify_auth = ShopifyAuth()
