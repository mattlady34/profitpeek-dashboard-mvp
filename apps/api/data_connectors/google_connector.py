"""
Google Ads API connector for campaigns and conversions
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import requests
from data_connectors.base_connector import BaseConnector

class GoogleConnector(BaseConnector):
    """Google Ads API connector"""
    
    def __init__(self, access_token: str, customer_id: str, developer_token: str):
        self.customer_id = customer_id
        self.developer_token = developer_token
        self.base_url = "https://googleads.googleapis.com/v14"
        super().__init__(access_token, base_url=self.base_url)
        self.session.headers.update({
            'developer-token': developer_token,
            'Authorization': f'Bearer {access_token}'
        })
    
    def authenticate(self) -> bool:
        """Authenticate with Google Ads API"""
        try:
            # Test with a simple query
            query = """
            SELECT customer.id, customer.descriptive_name
            FROM customer
            LIMIT 1
            """
            
            response = self.make_request('POST', f"{self.base_url}/customers/{self.customer_id}/googleAds:search", 
                                      json={'query': query})
            return response.status_code == 200
        except Exception as e:
            print(f"Google Ads authentication failed: {e}")
            return False
    
    def get_orders(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Google Ads doesn't have orders, return empty list"""
        return []
    
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get campaigns from Google Ads"""
        query = f"""
        SELECT 
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.start_date,
            campaign.end_date,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.clicks,
            metrics.impressions
        FROM campaign
        WHERE segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'
        """
        
        response = self.make_request('POST', f"{self.base_url}/customers/{self.customer_id}/googleAds:search", 
                                  json={'query': query})
        data = response.json()
        
        campaigns = []
        for row in data.get('results', []):
            campaign = row.get('campaign', {})
            metrics = row.get('metrics', {})
            
            campaigns.append({
                'id': campaign.get('id'),
                'name': campaign.get('name'),
                'status': campaign.get('status'),
                'start_date': campaign.get('startDate'),
                'end_date': campaign.get('endDate'),
                'cost': float(metrics.get('costMicros', 0)) / 1000000,  # Convert micros to dollars
                'conversions': float(metrics.get('conversions', 0)),
                'conversions_value': float(metrics.get('conversionsValue', 0)),
                'clicks': int(metrics.get('clicks', 0)),
                'impressions': int(metrics.get('impressions', 0))
            })
        
        return campaigns
    
    def get_products(self) -> List[Dict[str, Any]]:
        """Google Ads doesn't have products, return empty list"""
        return []
    
    def get_keywords(self, campaign_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get keywords for a campaign"""
        query = f"""
        SELECT 
            ad_group_criterion.criterion_id,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions,
            metrics.conversions_value
        FROM keyword_view
        WHERE segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'
        AND campaign.id = {campaign_id}
        """
        
        response = self.make_request('POST', f"{self.base_url}/customers/{self.customer_id}/googleAds:search", 
                                  json={'query': query})
        data = response.json()
        
        keywords = []
        for row in data.get('results', []):
            criterion = row.get('adGroupCriterion', {})
            keyword = criterion.get('keyword', {})
            metrics = row.get('metrics', {})
            
            keywords.append({
                'id': criterion.get('criterionId'),
                'text': keyword.get('text'),
                'match_type': keyword.get('matchType'),
                'cost': float(metrics.get('costMicros', 0)) / 1000000,
                'clicks': int(metrics.get('clicks', 0)),
                'impressions': int(metrics.get('impressions', 0)),
                'conversions': float(metrics.get('conversions', 0)),
                'conversions_value': float(metrics.get('conversionsValue', 0))
            })
        
        return keywords
