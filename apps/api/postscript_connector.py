"""
Postscript API connector for SMS campaigns and customer data
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class PostscriptConnector:
    """Postscript API connector"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.postscript.io/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """Test Postscript API connection"""
        try:
            response = self.session.get(f"{self.base_url}/account")
            return response.status_code == 200
        except Exception as e:
            print(f"Postscript connection test failed: {e}")
            return False
    
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get SMS campaigns from Postscript"""
        campaigns = []
        
        # Get campaigns
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'limit': 100
        }
        
        try:
            response = self.session.get(f"{self.base_url}/campaigns", params=params)
            response.raise_for_status()
            data = response.json()
            
            campaigns.extend(data.get('campaigns', []))
            return campaigns
            
        except Exception as e:
            print(f"Error fetching Postscript campaigns: {e}")
            return []
    
    def get_subscribers(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get subscribers from Postscript"""
        subscribers = []
        
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'limit': 100
        }
        
        try:
            response = self.session.get(f"{self.base_url}/subscribers", params=params)
            response.raise_for_status()
            data = response.json()
            
            subscribers.extend(data.get('subscribers', []))
            return subscribers
            
        except Exception as e:
            print(f"Error fetching Postscript subscribers: {e}")
            return []
    
    def get_messages(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get messages from Postscript"""
        messages = []
        
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'limit': 100
        }
        
        try:
            response = self.session.get(f"{self.base_url}/messages", params=params)
            response.raise_for_status()
            data = response.json()
            
            messages.extend(data.get('messages', []))
            return messages
            
        except Exception as e:
            print(f"Error fetching Postscript messages: {e}")
            return []
    
    def calculate_campaign_cost(self, campaign: Dict[str, Any]) -> float:
        """Calculate cost for a Postscript campaign"""
        # Postscript pricing is typically based on messages sent
        # This is an estimation - you'll need to adjust based on your plan
        sends = int(campaign.get('sends', 0))
        
        # Estimate cost based on typical Postscript pricing
        # Free tier: 100 messages/month
        # Paid tiers: ~$0.01 per SMS message
        
        if sends <= 100:
            return 0.0  # Free tier
        else:
            # Estimate: $0.01 per SMS
            return sends * 0.01
    
    def calculate_campaign_profit(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate profit for a Postscript campaign"""
        campaign_name = campaign.get('name', 'Unknown Campaign')
        sends = int(campaign.get('sends', 0))
        revenue = float(campaign.get('revenue', 0))
        
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
            'revenue': revenue,
            'estimated_cost': estimated_cost,
            'attributed_cogs': attributed_cogs,
            'total_costs': total_costs,
            'profit': profit,
            'roas': roas,
            'cost_per_message': estimated_cost / sends if sends > 0 else 0
        }
    
    def get_campaign_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Get metrics for a specific campaign"""
        try:
            response = self.session.get(f"{self.base_url}/campaigns/{campaign_id}/metrics")
            response.raise_for_status()
            data = response.json()
            return data.get('metrics', {})
        except Exception as e:
            print(f"Failed to get metrics for campaign {campaign_id}: {e}")
            return {}

# Test function
def test_postscript_connection():
    """Test Postscript connection with demo data"""
    print("Testing Postscript connection...")
    
    # Demo credentials (replace with real ones)
    api_key = "YOUR_API_KEY"
    
    connector = PostscriptConnector(api_key)
    
    if connector.test_connection():
        print("✅ Postscript connection successful!")
        
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
        print("❌ Postscript connection failed!")
        print("Please check your API key")

if __name__ == "__main__":
    test_postscript_connection()
