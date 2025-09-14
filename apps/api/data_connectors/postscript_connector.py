"""
Postscript API connector for SMS campaigns and customer data
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import requests
from .base_connector import BaseConnector

class PostscriptConnector(BaseConnector):
    """Postscript API connector"""
    
    def __init__(self, api_key: str):
        self.base_url = "https://api.postscript.io/v1"
        super().__init__(api_key, base_url=self.base_url)
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}'
        })
    
    def authenticate(self) -> bool:
        """Authenticate with Postscript API"""
        try:
            response = self.make_request('GET', f"{self.base_url}/account")
            return response.status_code == 200
        except Exception as e:
            print(f"Postscript authentication failed: {e}")
            return False
    
    def get_orders(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Postscript doesn't have orders, return empty list"""
        return []
    
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get SMS campaigns from Postscript"""
        campaigns = []
        
        # Get campaigns
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'limit': 100
        }
        
        response = self.make_request('GET', f"{self.base_url}/campaigns", params=params)
        data = response.json()
        
        campaigns.extend(data.get('campaigns', []))
        
        return campaigns
    
    def get_products(self) -> List[Dict[str, Any]]:
        """Postscript doesn't have products, return empty list"""
        return []
    
    def get_subscribers(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get subscribers from Postscript"""
        subscribers = []
        
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'limit': 100
        }
        
        response = self.make_request('GET', f"{self.base_url}/subscribers", params=params)
        data = response.json()
        
        subscribers.extend(data.get('subscribers', []))
        
        return subscribers
    
    def get_messages(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get messages from Postscript"""
        messages = []
        
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'limit': 100
        }
        
        response = self.make_request('GET', f"{self.base_url}/messages", params=params)
        data = response.json()
        
        messages.extend(data.get('messages', []))
        
        return messages
