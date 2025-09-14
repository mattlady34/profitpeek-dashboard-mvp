#!/usr/bin/env python3
"""
Test script for Klaviyo integration
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps', 'api'))

from klaviyo_connector import KlaviyoConnector
from datetime import datetime, timedelta

def test_klaviyo():
    """Test Klaviyo integration"""
    print("📧 Testing Klaviyo Integration")
    print("=" * 50)
    
    # You'll need to replace this with your actual API key
    api_key = input("Enter your Klaviyo API Key: ").strip()
    
    if not api_key:
        print("❌ Please provide your API key")
        return
    
    # Create connector
    connector = KlaviyoConnector(api_key)
    
    # Test connection
    print("\n1. Testing API connection...")
    if connector.test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
        return
    
    # Get campaigns from last 30 days
    print("\n2. Fetching campaigns...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    campaigns = connector.get_campaigns(start_date, end_date)
    print(f"Found {len(campaigns)} campaigns")
    
    if not campaigns:
        print("No campaigns found. This might be normal if:")
        print("- Your Klaviyo account is new")
        print("- No campaigns ran in the last 30 days")
        print("- API permissions are insufficient")
        return
    
    # Calculate profits for each campaign
    print("\n3. Calculating campaign profits...")
    total_cost = 0
    total_revenue = 0
    total_profit = 0
    
    for i, campaign in enumerate(campaigns[:5]):  # Show first 5 campaigns
        profit_data = connector.calculate_campaign_profit(campaign)
        
        print(f"\nCampaign {i+1}: {profit_data['campaign_name']}")
        print(f"  📧 Sends: {profit_data['sends']:,}")
        print(f"  👀 Opens: {profit_data['opens']:,}")
        print(f"  🖱️  Clicks: {profit_data['clicks']:,}")
        print(f"  📈 Revenue: ${profit_data['revenue']:.2f}")
        print(f"  💰 Cost: ${profit_data['estimated_cost']:.2f}")
        print(f"  💵 Profit: ${profit_data['profit']:.2f}")
        print(f"  📊 ROAS: {profit_data['roas']:.2f}")
        print(f"  📊 Open Rate: {profit_data['open_rate']:.1f}%")
        print(f"  📊 Click Rate: {profit_data['click_rate']:.1f}%")
        
        total_cost += profit_data['estimated_cost']
        total_revenue += profit_data['revenue']
        total_profit += profit_data['profit']
    
    # Get flows
    print(f"\n4. Fetching flows...")
    flows = connector.get_flows(start_date, end_date)
    print(f"Found {len(flows)} flows")
    
    # Get segments
    print(f"\n5. Fetching segments...")
    segments = connector.get_segments()
    print(f"Found {len(segments)} segments")
    
    # Summary
    print(f"\n📊 SUMMARY (Last 30 days)")
    print("=" * 30)
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"Overall ROAS: {total_revenue/total_cost:.2f}" if total_cost > 0 else "N/A")
    print(f"Profit Margin: {(total_profit/total_revenue*100):.1f}%" if total_revenue > 0 else "N/A")
    
    print(f"\n✅ Klaviyo integration test completed!")
    print("This data can now be integrated into ProfitPeek!")

if __name__ == "__main__":
    test_klaviyo()
