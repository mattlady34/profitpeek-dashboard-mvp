"""
Klaviyo API connector for email campaigns and customer data
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class KlaviyoConnector:
    """Klaviyo API connector"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://a.klaviyo.com/api"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Klaviyo-API-Key {api_key}',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """Test Klaviyo API connection"""
        try:
            response = self.session.get(f"{self.base_url}/accounts/")
            return response.status_code == 200
        except Exception as e:
            print(f"Klaviyo connection test failed: {e}")
            return False
    
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get email campaigns from Klaviyo"""
        campaigns = []
        
        # Get campaigns
        params = {
            'filter': f'greater-than(created,{start_date.isoformat()}),less-than(created,{end_date.isoformat()})',
            'page[size]': 100
        }
        
        try:
            response = self.session.get(f"{self.base_url}/campaigns/", params=params)
            response.raise_for_status()
            data = response.json()
            
            campaigns.extend(data.get('data', []))
            
            # Get metrics for each campaign
            for campaign in campaigns:
                metrics = self.get_campaign_metrics(campaign['id'])
                campaign['metrics'] = metrics
            
            return campaigns
            
        except Exception as e:
            print(f"Error fetching Klaviyo campaigns: {e}")
            return []
    
    def get_campaign_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Get metrics for a specific campaign"""
        try:
            response = self.session.get(f"{self.base_url}/campaigns/{campaign_id}/metrics/")
            response.raise_for_status()
            data = response.json()
            return data.get('data', {})
        except Exception as e:
            print(f"Failed to get metrics for campaign {campaign_id}: {e}")
            return {}
    
    def get_flows(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get flows from Klaviyo"""
        flows = []
        
        params = {
            'filter': f'greater-than(created,{start_date.isoformat()}),less-than(created,{end_date.isoformat()})',
            'page[size]': 100
        }
        
        try:
            response = self.session.get(f"{self.base_url}/flows/", params=params)
            response.raise_for_status()
            data = response.json()
            
            flows.extend(data.get('data', []))
            return flows
            
        except Exception as e:
            print(f"Error fetching Klaviyo flows: {e}")
            return []
    
    def get_segments(self) -> List[Dict[str, Any]]:
        """Get segments from Klaviyo"""
        segments = []
        
        params = {'page[size]': 100}
        
        try:
            response = self.session.get(f"{self.base_url}/segments/", params=params)
            response.raise_for_status()
            data = response.json()
            
            segments.extend(data.get('data', []))
            return segments
            
        except Exception as e:
            print(f"Error fetching Klaviyo segments: {e}")
            return []
    
    def get_products(self) -> List[Dict[str, Any]]:
        """Get products from Klaviyo"""
        products = []
        
        params = {'page[size]': 100}
        
        try:
            response = self.session.get(f"{self.base_url}/catalog-items/", params=params)
            response.raise_for_status()
            data = response.json()
            
            products.extend(data.get('data', []))
            return products
            
        except Exception as e:
            print(f"Error fetching Klaviyo products: {e}")
            return []
    
    def calculate_campaign_cost(self, campaign: Dict[str, Any]) -> float:
        """Calculate estimated cost for a Klaviyo campaign"""
        metrics = campaign.get('metrics', {})
        
        # Klaviyo pricing is typically based on contacts and sends
        # This is an estimation - you'll need to adjust based on your plan
        contacts = metrics.get('contacts', 0)
        sends = metrics.get('sends', 0)
        
        # Estimate cost based on typical Klaviyo pricing
        # Free tier: 500 contacts, 15,000 emails/month
        # Paid tiers: ~$20/month for 1,000 contacts, $0.0015 per email
        
        if contacts <= 500 and sends <= 15000:
            return 0.0  # Free tier
        else:
            # Estimate: $20 per 1,000 contacts + $0.0015 per email
            contact_cost = (contacts / 1000) * 20
            email_cost = sends * 0.0015
            return contact_cost + email_cost
    
    def calculate_campaign_profit(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate profit for a Klaviyo campaign"""
        metrics = campaign.get('metrics', {})
        
        # Get campaign data
        campaign_name = campaign.get('attributes', {}).get('name', 'Unknown Campaign')
        sends = int(metrics.get('sends', 0))
        opens = int(metrics.get('opens', 0))
        clicks = int(metrics.get('clicks', 0))
        revenue = float(metrics.get('revenue', 0))
        
        # Calculate estimated cost
        estimated_cost = self.calculate_campaign_cost(campaign)
        
        # Calculate attributed COGS (40% of revenue)
        attributed_cogs = revenue * 0.4
        
        total_costs = estimated_cost + attributed_cogs
        profit = revenue - total_costs
        roas = revenue / estimated_cost if estimated_cost > 0 else 0
        
        return {
            'campaign_id': campaign.get('id'),
            'campaign_name': campaign_name,
            'sends': sends,
            'opens': opens,
            'clicks': clicks,
            'revenue': revenue,
            'estimated_cost': estimated_cost,
            'attributed_cogs': attributed_cogs,
            'total_costs': total_costs,
            'profit': profit,
            'roas': roas,
            'open_rate': (opens / sends * 100) if sends > 0 else 0,
            'click_rate': (clicks / sends * 100) if sends > 0 else 0
        }

# Test function
def test_klaviyo_connection():
    """Test Klaviyo connection with demo data"""
    print("Testing Klaviyo connection...")
    
    # Demo credentials (replace with real ones)
    api_key = "YOUR_API_KEY"
    
    connector = KlaviyoConnector(api_key)
    
    if connector.test_connection():
        print("✅ Klaviyo connection successful!")
        
        # Test with last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        campaigns = connector.get_campaigns(start_date, end_date)
        print(f"Found {len(campaigns)} campaigns")
        
        # Calculate profits for each campaign
        for campaign in campaigns:
            profit_data = connector.calculate_campaign_profit(campaign)
            print(f"Campaign: {profit_data['campaign_name']}")
            print(f"  Sends: {profit_data['sends']:,}")
            print(f"  Revenue: ${profit_data['revenue']:.2f}")
            print(f"  Cost: ${profit_data['estimated_cost']:.2f}")
            print(f"  Profit: ${profit_data['profit']:.2f}")
            print(f"  ROAS: {profit_data['roas']:.2f}")
            print()
    else:
        print("❌ Klaviyo connection failed!")
        print("Please check your API key")

if __name__ == "__main__":
    test_klaviyo_connection()
