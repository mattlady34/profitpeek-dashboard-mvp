#!/usr/bin/env python3
"""
Test script for Meta Ads integration
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps', 'api'))

from meta_ads_connector import MetaAdsConnector
from datetime import datetime, timedelta

def test_meta_ads():
    """Test Meta Ads integration"""
    print("🔗 Testing Meta Ads Integration")
    print("=" * 50)
    
    # You'll need to replace these with your actual credentials
    access_token = input("Enter your Facebook Access Token: ").strip()
    ad_account_id = input("Enter your Ad Account ID: ").strip()
    
    if not access_token or not ad_account_id:
        print("❌ Please provide both access token and ad account ID")
        return
    
    # Create connector
    connector = MetaAdsConnector(access_token, ad_account_id)
    
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
        print("- Your ad account is new")
        print("- No campaigns ran in the last 30 days")
        print("- API permissions are insufficient")
        return
    
    # Calculate profits for each campaign
    print("\n3. Calculating campaign profits...")
    total_spend = 0
    total_revenue = 0
    total_profit = 0
    
    for i, campaign in enumerate(campaigns[:5]):  # Show first 5 campaigns
        profit_data = connector.calculate_campaign_profit(campaign)
        
        print(f"\nCampaign {i+1}: {profit_data['campaign_name']}")
        print(f"  💰 Ad Spend: ${profit_data['ad_spend']:.2f}")
        print(f"  📈 Revenue: ${profit_data['conversions_value']:.2f}")
        print(f"  💵 Profit: ${profit_data['profit']:.2f}")
        print(f"  📊 ROAS: {profit_data['roas']:.2f}")
        print(f"  👀 Impressions: {profit_data['impressions']:,}")
        print(f"  🖱️  Clicks: {profit_data['clicks']:,}")
        print(f"  🎯 Conversions: {profit_data['conversions']}")
        
        total_spend += profit_data['ad_spend']
        total_revenue += profit_data['conversions_value']
        total_profit += profit_data['profit']
    
    # Summary
    print(f"\n📊 SUMMARY (Last 30 days)")
    print("=" * 30)
    print(f"Total Ad Spend: ${total_spend:.2f}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"Overall ROAS: {total_revenue/total_spend:.2f}" if total_spend > 0 else "N/A")
    print(f"Profit Margin: {(total_profit/total_revenue*100):.1f}%" if total_revenue > 0 else "N/A")
    
    print(f"\n✅ Meta Ads integration test completed!")
    print("This data can now be integrated into ProfitPeek!")

if __name__ == "__main__":
    test_meta_ads()
