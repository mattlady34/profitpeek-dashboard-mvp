#!/usr/bin/env python3
"""
Test script for Google Ads integration
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps', 'api'))

from google_ads_connector import GoogleAdsConnector
from datetime import datetime, timedelta

def test_google_ads():
    """Test Google Ads integration"""
    print("🔍 Testing Google Ads Integration")
    print("=" * 50)
    
    # You'll need to replace these with your actual credentials
    access_token = input("Enter your Google Ads Access Token: ").strip()
    customer_id = input("Enter your Customer ID (e.g., 1234567890): ").strip()
    developer_token = input("Enter your Developer Token: ").strip()
    
    if not access_token or not customer_id or not developer_token:
        print("❌ Please provide all three credentials")
        return
    
    # Create connector
    connector = GoogleAdsConnector(access_token, customer_id, developer_token)
    
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
        print("- Your Google Ads account is new")
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
        print(f"  💰 Cost: ${profit_data['cost']:.2f}")
        print(f"  📈 Revenue: ${profit_data['conversions_value']:.2f}")
        print(f"  💵 Profit: ${profit_data['profit']:.2f}")
        print(f"  📊 ROAS: {profit_data['roas']:.2f}")
        print(f"  👀 Impressions: {profit_data['impressions']:,}")
        print(f"  🖱️  Clicks: {profit_data['clicks']:,}")
        print(f"  🎯 Conversions: {profit_data['conversions']}")
        
        total_cost += profit_data['cost']
        total_revenue += profit_data['conversions_value']
        total_profit += profit_data['profit']
    
    # Get keywords for first campaign
    if campaigns:
        print(f"\n4. Fetching keywords for '{campaigns[0]['name']}'...")
        keywords = connector.get_keywords(campaigns[0]['id'], start_date, end_date)
        print(f"Found {len(keywords)} keywords")
        
        if keywords:
            print("\nTop 5 keywords by cost:")
            sorted_keywords = sorted(keywords, key=lambda x: x['cost'], reverse=True)
            for i, keyword in enumerate(sorted_keywords[:5]):
                print(f"  {i+1}. {keyword['search_term']} - ${keyword['cost']:.2f}")
    
    # Summary
    print(f"\n📊 SUMMARY (Last 30 days)")
    print("=" * 30)
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"Overall ROAS: {total_revenue/total_cost:.2f}" if total_cost > 0 else "N/A")
    print(f"Profit Margin: {(total_profit/total_revenue*100):.1f}%" if total_revenue > 0 else "N/A")
    
    print(f"\n✅ Google Ads integration test completed!")
    print("This data can now be integrated into ProfitPeek!")

if __name__ == "__main__":
    test_google_ads()
