"""
Facebook Marketing API connector for ad campaigns and conversions
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import requests
from data_connectors.base_connector import BaseConnector

class FacebookConnector(BaseConnector):
    """Facebook Marketing API connector"""
    
    def __init__(self, access_token: str, ad_account_id: str):
        self.ad_account_id = ad_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
        super().__init__(access_token, base_url=self.base_url)
        self.session.params.update({'access_token': access_token})
    
    def authenticate(self) -> bool:
        """Authenticate with Facebook API"""
        try:
            response = self.make_request('GET', f"{self.base_url}/me")
            return response.status_code == 200
        except Exception as e:
            print(f"Facebook authentication failed: {e}")
            return False
    
    def get_orders(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Facebook doesn't have orders, return empty list"""
        return []
    
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get ad campaigns from Facebook"""
        campaigns = []
        
        # Get campaigns
        params = {
            'fields': 'id,name,status,created_time,updated_time',
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            }
        }
        
        response = self.make_request('GET', f"{self.base_url}/{self.ad_account_id}/campaigns", params=params)
        data = response.json()
        
        campaigns.extend(data.get('data', []))
        
        # Get insights for each campaign
        for campaign in campaigns:
            insights = self.get_campaign_insights(campaign['id'], start_date, end_date)
            campaign['insights'] = insights
        
        return campaigns
    
    def get_campaign_insights(self, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get insights for a specific campaign"""
        params = {
            'fields': 'impressions,clicks,spend,conversions,conversion_values',
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            },
            'level': 'campaign'
        }
        
        try:
            response = self.make_request('GET', f"{self.base_url}/{campaign_id}/insights", params=params)
            data = response.json()
            return data.get('data', [{}])[0] if data.get('data') else {}
        except Exception as e:
            print(f"Failed to get insights for campaign {campaign_id}: {e}")
            return {}
    
    def get_products(self) -> List[Dict[str, Any]]:
        """Facebook doesn't have products, return empty list"""
        return []
    
    def get_ad_sets(self, campaign_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get ad sets for a campaign"""
        params = {
            'fields': 'id,name,status,created_time,updated_time',
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            }
        }
        
        response = self.make_request('GET', f"{self.base_url}/{campaign_id}/adsets", params=params)
        data = response.json()
        
        return data.get('data', [])
    
    def get_ads(self, adset_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get ads for an ad set"""
        params = {
            'fields': 'id,name,status,created_time,updated_time',
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            }
        }
        
        response = self.make_request('GET', f"{self.base_url}/{adset_id}/ads", params=params)
        data = response.json()
        
        return data.get('data', [])
