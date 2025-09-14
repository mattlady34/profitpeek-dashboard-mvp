"""
Data integration service for managing multiple platform connections
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from data_connectors.shopify_connector import ShopifyConnector
from data_connectors.facebook_connector import FacebookConnector
from data_connectors.google_connector import GoogleConnector
from data_connectors.klaviyo_connector import KlaviyoConnector
from data_connectors.postscript_connector import PostscriptConnector
from profit_calculator import ProfitCalculator, OrderProfit, CampaignProfit

logger = logging.getLogger(__name__)

class DataIntegrationService:
    """Service for managing data integration across multiple platforms"""
    
    def __init__(self):
        self.connectors = {}
        self.profit_calculator = ProfitCalculator()
    
    def add_shopify_connection(self, shop_domain: str, access_token: str) -> bool:
        """Add Shopify connection"""
        try:
            connector = ShopifyConnector(shop_domain, access_token)
            if connector.test_connection():
                self.connectors['shopify'] = connector
                logger.info(f"Shopify connection added for {shop_domain}")
                return True
            else:
                logger.error(f"Failed to connect to Shopify for {shop_domain}")
                return False
        except Exception as e:
            logger.error(f"Error adding Shopify connection: {e}")
            return False
    
    def add_facebook_connection(self, access_token: str, ad_account_id: str) -> bool:
        """Add Facebook connection"""
        try:
            connector = FacebookConnector(access_token, ad_account_id)
            if connector.test_connection():
                self.connectors['facebook'] = connector
                logger.info(f"Facebook connection added for account {ad_account_id}")
                return True
            else:
                logger.error(f"Failed to connect to Facebook for account {ad_account_id}")
                return False
        except Exception as e:
            logger.error(f"Error adding Facebook connection: {e}")
            return False
    
    def add_google_connection(self, access_token: str, customer_id: str, developer_token: str) -> bool:
        """Add Google Ads connection"""
        try:
            connector = GoogleConnector(access_token, customer_id, developer_token)
            if connector.test_connection():
                self.connectors['google'] = connector
                logger.info(f"Google Ads connection added for customer {customer_id}")
                return True
            else:
                logger.error(f"Failed to connect to Google Ads for customer {customer_id}")
                return False
        except Exception as e:
            logger.error(f"Error adding Google Ads connection: {e}")
            return False
    
    def add_klaviyo_connection(self, api_key: str) -> bool:
        """Add Klaviyo connection"""
        try:
            connector = KlaviyoConnector(api_key)
            if connector.test_connection():
                self.connectors['klaviyo'] = connector
                logger.info("Klaviyo connection added")
                return True
            else:
                logger.error("Failed to connect to Klaviyo")
                return False
        except Exception as e:
            logger.error(f"Error adding Klaviyo connection: {e}")
            return False
    
    def add_postscript_connection(self, api_key: str) -> bool:
        """Add Postscript connection"""
        try:
            connector = PostscriptConnector(api_key)
            if connector.test_connection():
                self.connectors['postscript'] = connector
                logger.info("Postscript connection added")
                return True
            else:
                logger.error("Failed to connect to Postscript")
                return False
        except Exception as e:
            logger.error(f"Error adding Postscript connection: {e}")
            return False
    
    def sync_all_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Sync data from all connected platforms"""
        
        all_orders = []
        all_campaigns = []
        sync_results = {}
        
        # Sync orders from Shopify
        if 'shopify' in self.connectors:
            try:
                orders = self.connectors['shopify'].get_orders(start_date, end_date)
                all_orders.extend(orders)
                sync_results['shopify_orders'] = len(orders)
                logger.info(f"Synced {len(orders)} orders from Shopify")
            except Exception as e:
                logger.error(f"Error syncing Shopify orders: {e}")
                sync_results['shopify_orders'] = 0
        
        # Sync campaigns from Facebook
        if 'facebook' in self.connectors:
            try:
                campaigns = self.connectors['facebook'].get_campaigns(start_date, end_date)
                all_campaigns.extend(campaigns)
                sync_results['facebook_campaigns'] = len(campaigns)
                logger.info(f"Synced {len(campaigns)} campaigns from Facebook")
            except Exception as e:
                logger.error(f"Error syncing Facebook campaigns: {e}")
                sync_results['facebook_campaigns'] = 0
        
        # Sync campaigns from Google
        if 'google' in self.connectors:
            try:
                campaigns = self.connectors['google'].get_campaigns(start_date, end_date)
                all_campaigns.extend(campaigns)
                sync_results['google_campaigns'] = len(campaigns)
                logger.info(f"Synced {len(campaigns)} campaigns from Google")
            except Exception as e:
                logger.error(f"Error syncing Google campaigns: {e}")
                sync_results['google_campaigns'] = 0
        
        # Sync campaigns from Klaviyo
        if 'klaviyo' in self.connectors:
            try:
                campaigns = self.connectors['klaviyo'].get_campaigns(start_date, end_date)
                all_campaigns.extend(campaigns)
                sync_results['klaviyo_campaigns'] = len(campaigns)
                logger.info(f"Synced {len(campaigns)} campaigns from Klaviyo")
            except Exception as e:
                logger.error(f"Error syncing Klaviyo campaigns: {e}")
                sync_results['klaviyo_campaigns'] = 0
        
        # Sync campaigns from Postscript
        if 'postscript' in self.connectors:
            try:
                campaigns = self.connectors['postscript'].get_campaigns(start_date, end_date)
                all_campaigns.extend(campaigns)
                sync_results['postscript_campaigns'] = len(campaigns)
                logger.info(f"Synced {len(campaigns)} campaigns from Postscript")
            except Exception as e:
                logger.error(f"Error syncing Postscript campaigns: {e}")
                sync_results['postscript_campaigns'] = 0
        
        return {
            'orders': all_orders,
            'campaigns': all_campaigns,
            'sync_results': sync_results,
            'total_orders': len(all_orders),
            'total_campaigns': len(all_campaigns)
        }
    
    def calculate_profits(self, orders: List[Dict[str, Any]], campaigns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate profits for all orders and campaigns"""
        
        # Calculate order profits
        order_profits = []
        for order in orders:
            if order.get('platform') == 'shopify' or 'total_price' in order:
                profit = self.profit_calculator.calculate_order_profit(order, 'shopify')
                order_profits.append(profit)
            else:
                profit = self.profit_calculator.calculate_order_profit(order, order.get('platform', 'unknown'))
                order_profits.append(profit)
        
        # Calculate campaign profits
        campaign_profits = []
        for campaign in campaigns:
            platform = campaign.get('platform', 'unknown')
            if platform == 'facebook':
                profit = self.profit_calculator.calculate_campaign_profit(campaign, 'facebook')
                campaign_profits.append(profit)
            elif platform == 'google':
                profit = self.profit_calculator.calculate_campaign_profit(campaign, 'google')
                campaign_profits.append(profit)
            elif platform == 'klaviyo':
                profit = self.profit_calculator.calculate_campaign_profit(campaign, 'klaviyo')
                campaign_profits.append(profit)
            elif platform == 'postscript':
                profit = self.profit_calculator.calculate_campaign_profit(campaign, 'postscript')
                campaign_profits.append(profit)
            else:
                profit = self.profit_calculator.calculate_campaign_profit(campaign, platform)
                campaign_profits.append(profit)
        
        # Calculate total profits
        total_profit = self.profit_calculator.calculate_total_profit(order_profits, campaign_profits)
        
        return {
            'order_profits': order_profits,
            'campaign_profits': campaign_profits,
            'total_profit': total_profit
        }
    
    def get_connection_status(self) -> Dict[str, bool]:
        """Get status of all connections"""
        status = {}
        for platform, connector in self.connectors.items():
            try:
                status[platform] = connector.test_connection()
            except Exception as e:
                logger.error(f"Error testing {platform} connection: {e}")
                status[platform] = False
        return status
    
    def get_available_platforms(self) -> List[str]:
        """Get list of available platforms"""
        return list(self.connectors.keys())
    
    def remove_connection(self, platform: str) -> bool:
        """Remove a platform connection"""
        if platform in self.connectors:
            del self.connectors[platform]
            logger.info(f"Removed {platform} connection")
            return True
        return False
