"""
Shopify API connector for orders, products, and customer data
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import requests
from .base_connector import BaseConnector

class ShopifyConnector(BaseConnector):
    """Shopify API connector"""
    
    def __init__(self, shop_domain: str, access_token: str):
        self.shop_domain = shop_domain
        self.base_url = f"https://{shop_domain}.myshopify.com/admin/api/2023-10"
        super().__init__(access_token, base_url=self.base_url)
        self.session.headers.update({
            'X-Shopify-Access-Token': access_token
        })
    
    def authenticate(self) -> bool:
        """Authenticate with Shopify API"""
        try:
            response = self.make_request('GET', f"{self.base_url}/shop.json")
            return response.status_code == 200
        except Exception as e:
            print(f"Shopify authentication failed: {e}")
            return False
    
    def get_orders(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get orders from Shopify"""
        orders = []
        page_info = None
        
        while True:
            params = {
                'created_at_min': start_date.isoformat(),
                'created_at_max': end_date.isoformat(),
                'status': 'any',
                'limit': 250
            }
            
            if page_info:
                params['page_info'] = page_info
            
            response = self.make_request('GET', f"{self.base_url}/orders.json", params=params)
            data = response.json()
            
            orders.extend(data.get('orders', []))
            
            # Check for pagination
            link_header = response.headers.get('Link', '')
            if 'rel="next"' not in link_header:
                break
            
            # Extract page_info from Link header
            for link in link_header.split(','):
                if 'rel="next"' in link:
                    page_info = link.split(';')[0].strip('<>').split('page_info=')[1]
                    break
            else:
                break
        
        return orders
    
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Shopify doesn't have campaigns, return empty list"""
        return []
    
    def get_products(self) -> List[Dict[str, Any]]:
        """Get products from Shopify"""
        products = []
        page_info = None
        
        while True:
            params = {'limit': 250}
            if page_info:
                params['page_info'] = page_info
            
            response = self.make_request('GET', f"{self.base_url}/products.json", params=params)
            data = response.json()
            
            products.extend(data.get('products', []))
            
            # Check for pagination
            link_header = response.headers.get('Link', '')
            if 'rel="next"' not in link_header:
                break
            
            # Extract page_info from Link header
            for link in link_header.split(','):
                if 'rel="next"' in link:
                    page_info = link.split(';')[0].strip('<>').split('page_info=')[1]
                    break
            else:
                break
        
        return products
    
    def get_customers(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get customers from Shopify"""
        customers = []
        page_info = None
        
        while True:
            params = {
                'created_at_min': start_date.isoformat(),
                'created_at_max': end_date.isoformat(),
                'limit': 250
            }
            
            if page_info:
                params['page_info'] = page_info
            
            response = self.make_request('GET', f"{self.base_url}/customers.json", params=params)
            data = response.json()
            
            customers.extend(data.get('customers', []))
            
            # Check for pagination
            link_header = response.headers.get('Link', '')
            if 'rel="next"' not in link_header:
                break
            
            # Extract page_info from Link header
            for link in link_header.split(','):
                if 'rel="next"' in link:
                    page_info = link.split(';')[0].strip('<>').split('page_info=')[1]
                    break
            else:
                break
        
        return customers
