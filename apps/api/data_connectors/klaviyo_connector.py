"""
Klaviyo API connector for email campaigns and customer data
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import requests
from data_connectors.base_connector import BaseConnector

class KlaviyoConnector(BaseConnector):
    """Klaviyo API connector"""
    
    def __init__(self, api_key: str):
        self.base_url = "https://a.klaviyo.com/api"
        super().__init__(api_key, base_url=self.base_url)
        self.session.headers.update({
            'Authorization': f'Klaviyo-API-Key {api_key}'
        })
    
    def authenticate(self) -> bool:
        """Authenticate with Klaviyo API"""
        try:
            response = self.make_request('GET', f"{self.base_url}/accounts/")
            return response.status_code == 200
        except Exception as e:
            print(f"Klaviyo authentication failed: {e}")
            return False
    
    def get_orders(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Klaviyo doesn't have orders, return empty list"""
        return []
    
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get email campaigns from Klaviyo"""
        campaigns = []
        
        # Get campaigns
        params = {
            'filter': f'greater-than(created,{start_date.isoformat()}),less-than(created,{end_date.isoformat()})',
            'page[size]': 100
        }
        
        response = self.make_request('GET', f"{self.base_url}/campaigns/", params=params)
        data = response.json()
        
        campaigns.extend(data.get('data', []))
        
        # Get metrics for each campaign
        for campaign in campaigns:
            metrics = self.get_campaign_metrics(campaign['id'])
            campaign['metrics'] = metrics
        
        return campaigns
    
    def get_campaign_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Get metrics for a specific campaign"""
        try:
            response = self.make_request('GET', f"{self.base_url}/campaigns/{campaign_id}/metrics/")
            data = response.json()
            return data.get('data', {})
        except Exception as e:
            print(f"Failed to get metrics for campaign {campaign_id}: {e}")
            return {}
    
    def get_products(self) -> List[Dict[str, Any]]:
        """Get products from Klaviyo"""
        products = []
        
        params = {'page[size]': 100}
        
        response = self.make_request('GET', f"{self.base_url}/catalog-items/", params=params)
        data = response.json()
        
        products.extend(data.get('data', []))
        
        return products
    
    def get_flows(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get flows from Klaviyo"""
        flows = []
        
        params = {
            'filter': f'greater-than(created,{start_date.isoformat()}),less-than(created,{end_date.isoformat()})',
            'page[size]': 100
        }
        
        response = self.make_request('GET', f"{self.base_url}/flows/", params=params)
        data = response.json()
        
        flows.extend(data.get('data', []))
        
        return flows
    
    def get_segments(self) -> List[Dict[str, Any]]:
        """Get segments from Klaviyo"""
        segments = []
        
        params = {'page[size]': 100}
        
        response = self.make_request('GET', f"{self.base_url}/segments/", params=params)
        data = response.json()
        
        segments.extend(data.get('data', []))
        
        return segments
