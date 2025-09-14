"""
Profit calculation engine for unified revenue and cost analysis
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class OrderProfit:
    """Order-level profit calculation"""
    order_id: str
    platform: str
    revenue: float
    cogs: float
    shipping: float
    fees: float
    marketing_costs: float
    total_costs: float
    profit: float
    margin: float
    created_at: datetime

@dataclass
class CampaignProfit:
    """Campaign-level profit calculation"""
    campaign_id: str
    platform: str
    name: str
    ad_spend: float
    revenue: float
    attributed_costs: float
    total_costs: float
    profit: float
    roas: float
    created_at: datetime

class ProfitCalculator:
    """Main profit calculation engine"""
    
    def __init__(self, default_cogs_percentage: float = 0.4):
        self.default_cogs_percentage = default_cogs_percentage
        self.cost_attribution_window = timedelta(days=7)  # 7-day attribution window
    
    def calculate_order_profit(self, order: Dict[str, Any], platform: str = "shopify") -> OrderProfit:
        """Calculate profit for a single order"""
        
        if platform == "shopify":
            return self._calculate_shopify_order_profit(order)
        else:
            return self._calculate_generic_order_profit(order, platform)
    
    def _calculate_shopify_order_profit(self, order: Dict[str, Any]) -> OrderProfit:
        """Calculate profit for Shopify order"""
        
        # Revenue
        revenue = float(order.get('total_price', 0))
        
        # COGS calculation
        cogs = 0
        for line_item in order.get('line_items', []):
            item_price = float(line_item.get('price', 0))
            quantity = int(line_item.get('quantity', 1))
            # Use default COGS percentage if not specified
            item_cogs = item_price * quantity * self.default_cogs_percentage
            cogs += item_cogs
        
        # Shipping costs
        shipping = 0
        for shipping_line in order.get('shipping_lines', []):
            shipping += float(shipping_line.get('price', 0))
        
        # Fees (taxes + payment processing)
        fees = float(order.get('total_tax', 0))
        
        # Payment processing fees (estimated)
        gateway_fees = revenue * 0.029 + 0.30  # 2.9% + $0.30
        fees += gateway_fees
        
        # Marketing costs (will be calculated separately)
        marketing_costs = 0
        
        # Total costs
        total_costs = cogs + shipping + fees + marketing_costs
        
        # Profit calculation
        profit = revenue - total_costs
        margin = (profit / revenue * 100) if revenue > 0 else 0
        
        return OrderProfit(
            order_id=order.get('id', ''),
            platform='shopify',
            revenue=revenue,
            cogs=cogs,
            shipping=shipping,
            fees=fees,
            marketing_costs=marketing_costs,
            total_costs=total_costs,
            profit=profit,
            margin=margin,
            created_at=datetime.fromisoformat(order.get('created_at', '').replace('Z', '+00:00'))
        )
    
    def _calculate_generic_order_profit(self, order: Dict[str, Any], platform: str) -> OrderProfit:
        """Calculate profit for generic order"""
        
        revenue = float(order.get('revenue', 0))
        cogs = float(order.get('cogs', 0))
        shipping = float(order.get('shipping', 0))
        fees = float(order.get('fees', 0))
        marketing_costs = float(order.get('marketing_costs', 0))
        
        total_costs = cogs + shipping + fees + marketing_costs
        profit = revenue - total_costs
        margin = (profit / revenue * 100) if revenue > 0 else 0
        
        return OrderProfit(
            order_id=order.get('id', ''),
            platform=platform,
            revenue=revenue,
            cogs=cogs,
            shipping=shipping,
            fees=fees,
            marketing_costs=marketing_costs,
            total_costs=total_costs,
            profit=profit,
            margin=margin,
            created_at=datetime.fromisoformat(order.get('created_at', '').replace('Z', '+00:00'))
        )
    
    def calculate_campaign_profit(self, campaign: Dict[str, Any], platform: str) -> CampaignProfit:
        """Calculate profit for a campaign"""
        
        if platform == "facebook":
            return self._calculate_facebook_campaign_profit(campaign)
        elif platform == "google":
            return self._calculate_google_campaign_profit(campaign)
        elif platform == "klaviyo":
            return self._calculate_klaviyo_campaign_profit(campaign)
        elif platform == "postscript":
            return self._calculate_postscript_campaign_profit(campaign)
        else:
            return self._calculate_generic_campaign_profit(campaign, platform)
    
    def _calculate_facebook_campaign_profit(self, campaign: Dict[str, Any]) -> CampaignProfit:
        """Calculate profit for Facebook campaign"""
        
        ad_spend = float(campaign.get('insights', {}).get('spend', 0))
        revenue = float(campaign.get('insights', {}).get('conversion_values', 0))
        
        # Attributed costs (COGS for attributed orders)
        attributed_costs = revenue * self.default_cogs_percentage
        
        total_costs = ad_spend + attributed_costs
        profit = revenue - total_costs
        roas = revenue / ad_spend if ad_spend > 0 else 0
        
        return CampaignProfit(
            campaign_id=campaign.get('id', ''),
            platform='facebook',
            name=campaign.get('name', ''),
            ad_spend=ad_spend,
            revenue=revenue,
            attributed_costs=attributed_costs,
            total_costs=total_costs,
            profit=profit,
            roas=roas,
            created_at=datetime.fromisoformat(campaign.get('created_time', '').replace('Z', '+00:00'))
        )
    
    def _calculate_google_campaign_profit(self, campaign: Dict[str, Any]) -> CampaignProfit:
        """Calculate profit for Google Ads campaign"""
        
        ad_spend = float(campaign.get('cost', 0))
        revenue = float(campaign.get('conversions_value', 0))
        
        # Attributed costs (COGS for attributed orders)
        attributed_costs = revenue * self.default_cogs_percentage
        
        total_costs = ad_spend + attributed_costs
        profit = revenue - total_costs
        roas = revenue / ad_spend if ad_spend > 0 else 0
        
        return CampaignProfit(
            campaign_id=campaign.get('id', ''),
            platform='google',
            name=campaign.get('name', ''),
            ad_spend=ad_spend,
            revenue=revenue,
            attributed_costs=attributed_costs,
            total_costs=total_costs,
            profit=profit,
            roas=roas,
            created_at=datetime.fromisoformat(campaign.get('start_date', '').replace('Z', '+00:00'))
        )
    
    def _calculate_klaviyo_campaign_profit(self, campaign: Dict[str, Any]) -> CampaignProfit:
        """Calculate profit for Klaviyo email campaign"""
        
        # Klaviyo doesn't provide direct cost data, estimate based on sends
        metrics = campaign.get('metrics', {})
        sends = int(metrics.get('sends', 0))
        estimated_cost = sends * 0.001  # $0.001 per send estimate
        
        revenue = float(metrics.get('revenue', 0))
        attributed_costs = revenue * self.default_cogs_percentage
        
        total_costs = estimated_cost + attributed_costs
        profit = revenue - total_costs
        roas = revenue / estimated_cost if estimated_cost > 0 else 0
        
        return CampaignProfit(
            campaign_id=campaign.get('id', ''),
            platform='klaviyo',
            name=campaign.get('attributes', {}).get('name', ''),
            ad_spend=estimated_cost,
            revenue=revenue,
            attributed_costs=attributed_costs,
            total_costs=total_costs,
            profit=profit,
            roas=roas,
            created_at=datetime.fromisoformat(campaign.get('attributes', {}).get('created', '').replace('Z', '+00:00'))
        )
    
    def _calculate_postscript_campaign_profit(self, campaign: Dict[str, Any]) -> CampaignProfit:
        """Calculate profit for Postscript SMS campaign"""
        
        # Postscript cost estimation
        sends = int(campaign.get('sends', 0))
        estimated_cost = sends * 0.01  # $0.01 per SMS estimate
        
        revenue = float(campaign.get('revenue', 0))
        attributed_costs = revenue * self.default_cogs_percentage
        
        total_costs = estimated_cost + attributed_costs
        profit = revenue - total_costs
        roas = revenue / estimated_cost if estimated_cost > 0 else 0
        
        return CampaignProfit(
            campaign_id=campaign.get('id', ''),
            platform='postscript',
            name=campaign.get('name', ''),
            ad_spend=estimated_cost,
            revenue=revenue,
            attributed_costs=attributed_costs,
            total_costs=total_costs,
            profit=profit,
            roas=roas,
            created_at=datetime.fromisoformat(campaign.get('created_at', '').replace('Z', '+00:00'))
        )
    
    def _calculate_generic_campaign_profit(self, campaign: Dict[str, Any], platform: str) -> CampaignProfit:
        """Calculate profit for generic campaign"""
        
        ad_spend = float(campaign.get('ad_spend', 0))
        revenue = float(campaign.get('revenue', 0))
        attributed_costs = float(campaign.get('attributed_costs', 0))
        
        total_costs = ad_spend + attributed_costs
        profit = revenue - total_costs
        roas = revenue / ad_spend if ad_spend > 0 else 0
        
        return CampaignProfit(
            campaign_id=campaign.get('id', ''),
            platform=platform,
            name=campaign.get('name', ''),
            ad_spend=ad_spend,
            revenue=revenue,
            attributed_costs=attributed_costs,
            total_costs=total_costs,
            profit=profit,
            roas=roas,
            created_at=datetime.fromisoformat(campaign.get('created_at', '').replace('Z', '+00:00'))
        )
    
    def calculate_total_profit(self, orders: List[OrderProfit], campaigns: List[CampaignProfit]) -> Dict[str, Any]:
        """Calculate total profit across all orders and campaigns"""
        
        total_revenue = sum(order.revenue for order in orders)
        total_costs = sum(order.total_costs for order in orders)
        total_marketing_costs = sum(campaign.ad_spend for campaign in campaigns)
        
        total_profit = total_revenue - total_costs - total_marketing_costs
        total_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'total_costs': total_costs,
            'total_marketing_costs': total_marketing_costs,
            'total_profit': total_profit,
            'total_margin': total_margin,
            'order_count': len(orders),
            'campaign_count': len(campaigns)
        }
