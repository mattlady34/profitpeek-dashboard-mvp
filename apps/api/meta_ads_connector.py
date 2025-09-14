"""
Meta Ads (Facebook) API connector for ad campaigns and conversions
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class MetaAdsConnector:
    """Meta Ads API connector"""
    
    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
        self.session = requests.Session()
        self.session.params.update({'access_token': access_token})
    
    def test_connection(self) -> bool:
        """Test Meta Ads API connection"""
        try:
            response = self.session.get(f"{self.base_url}/me")
            return response.status_code == 200
        except Exception as e:
            print(f"Meta Ads connection test failed: {e}")
            return False
    
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get ad campaigns from Meta Ads"""
        campaigns = []
        
        # Get campaigns
        params = {
            'fields': 'id,name,status,created_time,updated_time',
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            }
        }
        
        try:
            response = self.session.get(f"{self.base_url}/{self.ad_account_id}/campaigns", params=params)
            response.raise_for_status()
            data = response.json()
            
            campaigns.extend(data.get('data', []))
            
            # Get insights for each campaign
            for campaign in campaigns:
                insights = self.get_campaign_insights(campaign['id'], start_date, end_date)
                campaign['insights'] = insights
            
            return campaigns
            
        except Exception as e:
            print(f"Error fetching Meta Ads campaigns: {e}")
            return []
    
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
            response = self.session.get(f"{self.base_url}/{campaign_id}/insights", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [{}])[0] if data.get('data') else {}
        except Exception as e:
            print(f"Failed to get insights for campaign {campaign_id}: {e}")
            return {}
    
    def get_ad_sets(self, campaign_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get ad sets for a campaign"""
        params = {
            'fields': 'id,name,status,created_time,updated_time',
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            }
        }
        
        try:
            response = self.session.get(f"{self.base_url}/{campaign_id}/adsets", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching ad sets for campaign {campaign_id}: {e}")
            return []
    
    def get_ads(self, adset_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get ads for an ad set"""
        params = {
            'fields': 'id,name,status,created_time,updated_time',
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            }
        }
        
        try:
            response = self.session.get(f"{self.base_url}/{adset_id}/ads", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching ads for ad set {adset_id}: {e}")
            return []
    
    def calculate_campaign_profit(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate profit for a Meta Ads campaign"""
        insights = campaign.get('insights', {})
        
        ad_spend = float(insights.get('spend', 0))
        conversions_value = float(insights.get('conversion_values', 0))
        
        # Calculate attributed COGS (40% of conversion value)
        attributed_cogs = conversions_value * 0.4
        
        total_costs = ad_spend + attributed_cogs
        profit = conversions_value - total_costs
        roas = conversions_value / ad_spend if ad_spend > 0 else 0
        
        return {
            'campaign_id': campaign.get('id'),
            'campaign_name': campaign.get('name'),
            'ad_spend': ad_spend,
            'conversions_value': conversions_value,
            'attributed_cogs': attributed_cogs,
            'total_costs': total_costs,
            'profit': profit,
            'roas': roas,
            'impressions': int(insights.get('impressions', 0)),
            'clicks': int(insights.get('clicks', 0)),
            'conversions': int(insights.get('conversions', 0))
        }

# Test function
def test_meta_ads_connection():
    """Test Meta Ads connection with demo data"""
    print("Testing Meta Ads connection...")
    
    # Demo credentials (replace with real ones)
    access_token = "YOUR_ACCESS_TOKEN"
    ad_account_id = "YOUR_AD_ACCOUNT_ID"
    
    connector = MetaAdsConnector(access_token, ad_account_id)
    
    if connector.test_connection():
        print("✅ Meta Ads connection successful!")
        
        # Test with last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        campaigns = connector.get_campaigns(start_date, end_date)
        print(f"Found {len(campaigns)} campaigns")
        
        # Calculate profits for each campaign
        for campaign in campaigns:
            profit_data = connector.calculate_campaign_profit(campaign)
            print(f"Campaign: {profit_data['campaign_name']}")
            print(f"  Ad Spend: ${profit_data['ad_spend']:.2f}")
            print(f"  Revenue: ${profit_data['conversions_value']:.2f}")
            print(f"  Profit: ${profit_data['profit']:.2f}")
            print(f"  ROAS: {profit_data['roas']:.2f}")
            print()
    else:
        print("❌ Meta Ads connection failed!")
        print("Please check your access token and ad account ID")

if __name__ == "__main__":
    test_meta_ads_connection()
