"""
Advanced Profit Analytics Engine with sophisticated calculations and insights
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ProfitInsight:
    """Profit insight with recommendations"""
    insight_type: str
    title: str
    description: str
    impact: str  # 'high', 'medium', 'low'
    recommendation: str
    potential_savings: float = 0.0
    confidence: float = 0.0

@dataclass
class TrendAnalysis:
    """Trend analysis result"""
    metric: str
    trend_direction: str  # 'up', 'down', 'stable'
    change_percentage: float
    confidence: float
    forecast: List[float]

class AdvancedProfitAnalytics:
    """Advanced profit analytics with sophisticated calculations"""
    
    def __init__(self):
        self.data_cache = {}
        self.insights = []
        self.trends = {}
    
    def calculate_advanced_metrics(self, platform_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Calculate advanced profit metrics across all platforms"""
        metrics = {
            'total_revenue': 0.0,
            'total_costs': 0.0,
            'net_profit': 0.0,
            'profit_margin': 0.0,
            'roas': 0.0,
            'platform_breakdown': {},
            'cost_efficiency': {},
            'revenue_attribution': {},
            'profit_trends': {},
            'optimization_opportunities': []
        }
        
        # Calculate platform-level metrics
        for platform, campaigns in platform_data.items():
            platform_metrics = self._calculate_platform_metrics(platform, campaigns)
            metrics['platform_breakdown'][platform] = platform_metrics
            
            # Aggregate totals
            metrics['total_revenue'] += platform_metrics['total_revenue']
            metrics['total_costs'] += platform_metrics['total_costs']
            metrics['net_profit'] += platform_metrics['net_profit']
        
        # Calculate overall metrics
        if metrics['total_revenue'] > 0:
            metrics['profit_margin'] = (metrics['net_profit'] / metrics['total_revenue']) * 100
        
        if metrics['total_costs'] > 0:
            metrics['roas'] = metrics['total_revenue'] / metrics['total_costs']
        
        # Calculate cost efficiency
        metrics['cost_efficiency'] = self._calculate_cost_efficiency(platform_data)
        
        # Calculate revenue attribution
        metrics['revenue_attribution'] = self._calculate_revenue_attribution(platform_data)
        
        # Generate insights
        metrics['optimization_opportunities'] = self._generate_optimization_insights(platform_data)
        
        return metrics
    
    def _calculate_platform_metrics(self, platform: str, campaigns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate metrics for a specific platform"""
        if not campaigns:
            return {
                'total_revenue': 0.0,
                'total_costs': 0.0,
                'net_profit': 0.0,
                'campaign_count': 0,
                'avg_roas': 0.0,
                'best_campaign': None,
                'worst_campaign': None
            }
        
        total_revenue = sum(c.get('revenue', 0) for c in campaigns)
        total_costs = sum(c.get('cost', 0) for c in campaigns)
        net_profit = total_revenue - total_costs
        
        # Calculate ROAS for each campaign
        campaign_roas = []
        for campaign in campaigns:
            cost = campaign.get('cost', 0)
            revenue = campaign.get('revenue', 0)
            if cost > 0:
                campaign_roas.append(revenue / cost)
        
        avg_roas = np.mean(campaign_roas) if campaign_roas else 0
        
        # Find best and worst campaigns
        best_campaign = max(campaigns, key=lambda x: x.get('revenue', 0) - x.get('cost', 0)) if campaigns else None
        worst_campaign = min(campaigns, key=lambda x: x.get('revenue', 0) - x.get('cost', 0)) if campaigns else None
        
        return {
            'total_revenue': total_revenue,
            'total_costs': total_costs,
            'net_profit': net_profit,
            'campaign_count': len(campaigns),
            'avg_roas': avg_roas,
            'best_campaign': best_campaign,
            'worst_campaign': worst_campaign
        }
    
    def _calculate_cost_efficiency(self, platform_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Calculate cost efficiency metrics"""
        efficiency = {}
        
        for platform, campaigns in platform_data.items():
            if not campaigns:
                continue
            
            # Calculate cost per acquisition (CPA)
            total_cost = sum(c.get('cost', 0) for c in campaigns)
            total_conversions = sum(c.get('conversions', 0) for c in campaigns)
            cpa = total_cost / total_conversions if total_conversions > 0 else 0
            
            # Calculate cost per click (CPC)
            total_clicks = sum(c.get('clicks', 0) for c in campaigns)
            cpc = total_cost / total_clicks if total_clicks > 0 else 0
            
            # Calculate cost per impression (CPM)
            total_impressions = sum(c.get('impressions', 0) for c in campaigns)
            cpm = (total_cost / total_impressions) * 1000 if total_impressions > 0 else 0
            
            efficiency[platform] = {
                'cpa': cpa,
                'cpc': cpc,
                'cpm': cpm,
                'conversion_rate': (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            }
        
        return efficiency
    
    def _calculate_revenue_attribution(self, platform_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Calculate revenue attribution across platforms"""
        total_revenue = sum(
            sum(c.get('revenue', 0) for c in campaigns)
            for campaigns in platform_data.values()
        )
        
        attribution = {}
        for platform, campaigns in platform_data.items():
            platform_revenue = sum(c.get('revenue', 0) for c in campaigns)
            attribution[platform] = {
                'revenue': platform_revenue,
                'percentage': (platform_revenue / total_revenue * 100) if total_revenue > 0 else 0
            }
        
        return attribution
    
    def _generate_optimization_insights(self, platform_data: Dict[str, List[Dict[str, Any]]]) -> List[ProfitInsight]:
        """Generate optimization insights and recommendations"""
        insights = []
        
        # Analyze each platform
        for platform, campaigns in platform_data.items():
            if not campaigns:
                continue
            
            # Find low-performing campaigns
            low_performers = [c for c in campaigns if c.get('revenue', 0) - c.get('cost', 0) < 0]
            if low_performers:
                total_loss = sum(c.get('cost', 0) - c.get('revenue', 0) for c in low_performers)
                insights.append(ProfitInsight(
                    insight_type='cost_optimization',
                    title=f'Low-performing campaigns in {platform}',
                    description=f'{len(low_performers)} campaigns are losing money',
                    impact='high',
                    recommendation=f'Consider pausing or optimizing {len(low_performers)} campaigns',
                    potential_savings=total_loss,
                    confidence=0.8
                ))
            
            # Find high-performing campaigns
            high_performers = [c for c in campaigns if c.get('revenue', 0) - c.get('cost', 0) > 0]
            if high_performers:
                total_profit = sum(c.get('revenue', 0) - c.get('cost', 0) for c in high_performers)
                insights.append(ProfitInsight(
                    insight_type='scaling_opportunity',
                    title=f'High-performing campaigns in {platform}',
                    description=f'{len(high_performers)} campaigns are profitable',
                    impact='medium',
                    recommendation=f'Consider scaling up budget for {len(high_performers)} profitable campaigns',
                    potential_savings=total_profit * 0.2,  # 20% potential increase
                    confidence=0.7
                ))
        
        # Cross-platform insights
        platform_profits = {}
        for platform, campaigns in platform_data.items():
            platform_profits[platform] = sum(c.get('revenue', 0) - c.get('cost', 0) for c in campaigns)
        
        if platform_profits:
            best_platform = max(platform_profits, key=platform_profits.get)
            worst_platform = min(platform_profits, key=platform_profits.get)
            
            if platform_profits[best_platform] > platform_profits[worst_platform]:
                insights.append(ProfitInsight(
                    insight_type='budget_reallocation',
                    title='Budget reallocation opportunity',
                    description=f'{best_platform} is significantly more profitable than {worst_platform}',
                    impact='high',
                    recommendation=f'Consider reallocating budget from {worst_platform} to {best_platform}',
                    potential_savings=abs(platform_profits[best_platform] - platform_profits[worst_platform]) * 0.1,
                    confidence=0.6
                ))
        
        return insights
    
    def analyze_trends(self, historical_data: List[Dict[str, Any]], days: int = 30) -> Dict[str, TrendAnalysis]:
        """Analyze trends in historical data"""
        trends = {}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(historical_data)
        if df.empty:
            return trends
        
        # Analyze key metrics
        metrics = ['revenue', 'cost', 'profit', 'roas']
        
        for metric in metrics:
            if metric in df.columns:
                trend = self._calculate_trend(df[metric], days)
                trends[metric] = trend
        
        return trends
    
    def _calculate_trend(self, data: pd.Series, days: int) -> TrendAnalysis:
        """Calculate trend for a specific metric"""
        if len(data) < 2:
            return TrendAnalysis(
                metric=data.name if hasattr(data, 'name') else 'unknown',
                trend_direction='stable',
                change_percentage=0.0,
                confidence=0.0,
                forecast=[]
            )
        
        # Calculate trend direction
        recent_data = data.tail(days)
        if len(recent_data) < 2:
            recent_data = data.tail(min(len(data), 7))
        
        # Simple linear trend
        x = np.arange(len(recent_data))
        y = recent_data.values
        
        if len(y) > 1:
            slope = np.polyfit(x, y, 1)[0]
            change_percentage = (slope / np.mean(y)) * 100 if np.mean(y) != 0 else 0
            
            if change_percentage > 5:
                trend_direction = 'up'
            elif change_percentage < -5:
                trend_direction = 'down'
            else:
                trend_direction = 'stable'
            
            # Simple forecast (next 7 days)
            forecast = [y[-1] + slope * i for i in range(1, 8)]
            
            # Confidence based on data consistency
            confidence = min(1.0, len(recent_data) / 30)
        else:
            trend_direction = 'stable'
            change_percentage = 0.0
            forecast = []
            confidence = 0.0
        
        return TrendAnalysis(
            metric=data.name if hasattr(data, 'name') else 'unknown',
            trend_direction=trend_direction,
            change_percentage=change_percentage,
            confidence=confidence,
            forecast=forecast
        )
    
    def generate_forecast(self, historical_data: List[Dict[str, Any]], days_ahead: int = 30) -> Dict[str, List[float]]:
        """Generate forecast for key metrics"""
        if not historical_data:
            return {}
        
        df = pd.DataFrame(historical_data)
        forecasts = {}
        
        # Forecast key metrics
        metrics = ['revenue', 'cost', 'profit']
        
        for metric in metrics:
            if metric in df.columns:
                # Simple moving average forecast
                recent_data = df[metric].tail(30)
                if len(recent_data) > 0:
                    avg_value = recent_data.mean()
                    forecasts[metric] = [avg_value] * days_ahead
        
        return forecasts
    
    def get_optimization_recommendations(self, platform_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Get specific optimization recommendations"""
        recommendations = []
        
        for platform, campaigns in platform_data.items():
            if not campaigns:
                continue
            
            # Sort campaigns by profit
            sorted_campaigns = sorted(campaigns, key=lambda x: x.get('revenue', 0) - x.get('cost', 0), reverse=True)
            
            # Top 3 recommendations
            for i, campaign in enumerate(sorted_campaigns[:3]):
                profit = campaign.get('revenue', 0) - campaign.get('cost', 0)
                roas = campaign.get('revenue', 0) / campaign.get('cost', 0) if campaign.get('cost', 0) > 0 else 0
                
                if profit > 0:
                    recommendations.append({
                        'platform': platform,
                        'campaign': campaign.get('name', 'Unknown'),
                        'action': 'scale_up',
                        'current_profit': profit,
                        'current_roas': roas,
                        'recommended_budget_increase': campaign.get('cost', 0) * 0.2,
                        'expected_profit_increase': profit * 0.2
                    })
                elif i >= len(sorted_campaigns) - 3:  # Bottom 3
                    recommendations.append({
                        'platform': platform,
                        'campaign': campaign.get('name', 'Unknown'),
                        'action': 'pause_or_optimize',
                        'current_profit': profit,
                        'current_roas': roas,
                        'recommended_action': 'Pause campaign or optimize targeting',
                        'potential_savings': abs(profit)
                    })
        
        return recommendations

# Example usage
def main():
    """Example usage of advanced profit analytics"""
    analytics = AdvancedProfitAnalytics()
    
    # Sample data
    platform_data = {
        'shopify': [
            {'name': 'Product A', 'revenue': 1000, 'cost': 600, 'conversions': 10, 'clicks': 100, 'impressions': 1000},
            {'name': 'Product B', 'revenue': 800, 'cost': 500, 'conversions': 8, 'clicks': 80, 'impressions': 800}
        ],
        'meta_ads': [
            {'name': 'Campaign 1', 'revenue': 500, 'cost': 200, 'conversions': 5, 'clicks': 50, 'impressions': 500},
            {'name': 'Campaign 2', 'revenue': 300, 'cost': 150, 'conversions': 3, 'clicks': 30, 'impressions': 300}
        ]
    }
    
    # Calculate advanced metrics
    metrics = analytics.calculate_advanced_metrics(platform_data)
    print("Advanced Metrics:", metrics)
    
    # Generate insights
    insights = analytics._generate_optimization_insights(platform_data)
    print("Optimization Insights:", insights)
    
    # Get recommendations
    recommendations = analytics.get_optimization_recommendations(platform_data)
    print("Recommendations:", recommendations)

if __name__ == "__main__":
    main()
