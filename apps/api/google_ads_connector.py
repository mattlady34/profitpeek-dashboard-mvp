"""
Google Ads API connector for campaigns and conversions
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class GoogleAdsConnector:
    """Google Ads API connector"""
    
    def __init__(self, access_token: str, customer_id: str, developer_token: str):
        self.access_token = access_token
        self.customer_id = customer_id
        self.developer_token = developer_token
        self.base_url = "https://googleads.googleapis.com/v14"
        self.session = requests.Session()
        self.session.headers.update({
            'developer-token': developer_token,
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """Test Google Ads API connection"""
        try:
            # Test with a simple query
            query = """
            SELECT customer.id, customer.descriptive_name
            FROM customer
            LIMIT 1
            """
            
            response = self.session.post(f"{self.base_url}/customers/{self.customer_id}/googleAds:search", 
                                      json={'query': query})
            return response.status_code == 200
        except Exception as e:
            print(f"Google Ads connection test failed: {e}")
            return False
    
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
        
        try:
            response = self.session.post(f"{self.base_url}/customers/{self.customer_id}/googleAds:search", 
                                      json={'query': query})
            response.raise_for_status()
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
            
        except Exception as e:
            print(f"Error fetching Google Ads campaigns: {e}")
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
        
        try:
            response = self.session.post(f"{self.base_url}/customers/{self.customer_id}/googleAds:search", 
                                      json={'query': query})
            response.raise_for_status()
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
            
        except Exception as e:
            print(f"Error fetching keywords for campaign {campaign_id}: {e}")
            return []
    
    def get_ad_groups(self, campaign_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get ad groups for a campaign"""
        query = f"""
        SELECT 
            ad_group.id,
            ad_group.name,
            ad_group.status,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions,
            metrics.conversions_value
        FROM ad_group
        WHERE segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'
        AND campaign.id = {campaign_id}
        """
        
        try:
            response = self.session.post(f"{self.base_url}/customers/{self.customer_id}/googleAds:search", 
                                      json={'query': query})
            response.raise_for_status()
            data = response.json()
            
            ad_groups = []
            for row in data.get('results', []):
                ad_group = row.get('adGroup', {})
                metrics = row.get('metrics', {})
                
                ad_groups.append({
                    'id': ad_group.get('id'),
                    'name': ad_group.get('name'),
                    'status': ad_group.get('status'),
                    'cost': float(metrics.get('costMicros', 0)) / 1000000,
                    'clicks': int(metrics.get('clicks', 0)),
                    'impressions': int(metrics.get('impressions', 0)),
                    'conversions': float(metrics.get('conversions', 0)),
                    'conversions_value': float(metrics.get('conversionsValue', 0))
                })
            
            return ad_groups
            
        except Exception as e:
            print(f"Error fetching ad groups for campaign {campaign_id}: {e}")
            return []
    
    def calculate_campaign_profit(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate profit for a Google Ads campaign"""
        cost = campaign.get('cost', 0)
        conversions_value = campaign.get('conversions_value', 0)
        
        # Calculate attributed COGS (40% of conversion value)
        attributed_cogs = conversions_value * 0.4
        
        total_costs = cost + attributed_cogs
        profit = conversions_value - total_costs
        roas = conversions_value / cost if cost > 0 else 0
        
        return {
            'campaign_id': campaign.get('id'),
            'campaign_name': campaign.get('name'),
            'cost': cost,
            'conversions_value': conversions_value,
            'attributed_cogs': attributed_cogs,
            'total_costs': total_costs,
            'profit': profit,
            'roas': roas,
            'clicks': campaign.get('clicks', 0),
            'impressions': campaign.get('impressions', 0),
            'conversions': campaign.get('conversions', 0)
        }
    
    def get_search_terms(self, campaign_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get search terms for a campaign"""
        query = f"""
        SELECT 
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions,
            metrics.conversions_value
        FROM search_term_view
        WHERE segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'
        AND campaign.id = {campaign_id}
        """
        
        try:
            response = self.session.post(f"{self.base_url}/customers/{self.customer_id}/googleAds:search", 
                                      json={'query': query})
            response.raise_for_status()
            data = response.json()
            
            search_terms = []
            for row in data.get('results', []):
                search_term = row.get('searchTermView', {})
                metrics = row.get('metrics', {})
                
                search_terms.append({
                    'search_term': search_term.get('searchTerm'),
                    'cost': float(metrics.get('costMicros', 0)) / 1000000,
                    'clicks': int(metrics.get('clicks', 0)),
                    'impressions': int(metrics.get('impressions', 0)),
                    'conversions': float(metrics.get('conversions', 0)),
                    'conversions_value': float(metrics.get('conversionsValue', 0))
                })
            
            return search_terms
            
        except Exception as e:
            print(f"Error fetching search terms for campaign {campaign_id}: {e}")
            return []

# Test function
def test_google_ads_connection():
    """Test Google Ads connection with demo data"""
    print("Testing Google Ads connection...")
    
    # Demo credentials (replace with real ones)
    access_token = "YOUR_ACCESS_TOKEN"
    customer_id = "YOUR_CUSTOMER_ID"
    developer_token = "YOUR_DEVELOPER_TOKEN"
    
    connector = GoogleAdsConnector(access_token, customer_id, developer_token)
    
    if connector.test_connection():
        print("✅ Google Ads connection successful!")
        
        # Test with last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        campaigns = connector.get_campaigns(start_date, end_date)
        print(f"Found {len(campaigns)} campaigns")
        
        # Calculate profits for each campaign
        for campaign in campaigns:
            profit_data = connector.calculate_campaign_profit(campaign)
            print(f"Campaign: {profit_data['campaign_name']}")
            print(f"  Cost: ${profit_data['cost']:.2f}")
            print(f"  Revenue: ${profit_data['conversions_value']:.2f}")
            print(f"  Profit: ${profit_data['profit']:.2f}")
            print(f"  ROAS: {profit_data['roas']:.2f}")
            print()
    else:
        print("❌ Google Ads connection failed!")
        print("Please check your access token, customer ID, and developer token")

if __name__ == "__main__":
    test_google_ads_connection()
