"""Currency conversion and normalization utilities."""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, Optional
import httpx

from ..config.settings import get_settings

settings = get_settings()


class CurrencyConverter:
    """Handles currency conversion and normalization."""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    async def normalize_amount(
        self, 
        amount: Decimal, 
        from_currency: str, 
        to_currency: str
    ) -> Decimal:
        """Normalize amount from one currency to another."""
        if from_currency == to_currency:
            return amount
        
        rate = await self.get_exchange_rate(from_currency, to_currency)
        if rate is None:
            # If we can't get rate, return original amount
            return amount
        
        converted = amount * rate
        return converted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    async def get_exchange_rate(
        self, 
        from_currency: str, 
        to_currency: str
    ) -> Optional[Decimal]:
        """Get exchange rate between currencies."""
        cache_key = f"{from_currency}_{to_currency}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if self._is_cache_valid(cached_data):
                return cached_data['rate']
        
        # Fetch from API
        rate = await self._fetch_exchange_rate(from_currency, to_currency)
        if rate is not None:
            self.cache[cache_key] = {
                'rate': rate,
                'timestamp': self._get_current_timestamp()
            }
        
        return rate
    
    async def _fetch_exchange_rate(
        self, 
        from_currency: str, 
        to_currency: str
    ) -> Optional[Decimal]:
        """Fetch exchange rate from external API."""
        # Using a free exchange rate API
        # In production, you might want to use a more reliable service
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                rates = data.get('rates', {})
                rate = rates.get(to_currency)
                
                if rate:
                    return Decimal(str(rate))
                
                return None
        except Exception:
            return None
    
    def _is_cache_valid(self, cached_data: Dict[str, Any]) -> bool:
        """Check if cached data is still valid."""
        current_time = self._get_current_timestamp()
        return (current_time - cached_data['timestamp']) < self.cache_ttl
    
    def _get_current_timestamp(self) -> int:
        """Get current timestamp."""
        import time
        return int(time.time())


def normalize_amount(amount: str | Decimal, currency: str) -> Decimal:
    """Normalize amount string to Decimal."""
    if isinstance(amount, str):
        return Decimal(amount)
    return amount


def convert_currency(
    amount: Decimal, 
    from_currency: str, 
    to_currency: str, 
    rate: Optional[Decimal] = None
) -> Decimal:
    """Convert amount between currencies using provided rate."""
    if from_currency == to_currency:
        return amount
    
    if rate is None:
        # Return original amount if no rate provided
        return amount
    
    converted = amount * rate
    return converted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def format_currency(amount: Decimal, currency: str) -> str:
    """Format amount as currency string."""
    return f"{currency} {amount:.2f}"


def extract_amount_from_price_set(
    price_set: Dict[str, Any], 
    currency: str
) -> Decimal:
    """Extract amount from Shopify price set for given currency."""
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


# Global converter instance
currency_converter = CurrencyConverter()
