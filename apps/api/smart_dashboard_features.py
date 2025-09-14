"""
Smart Dashboard Features with real-time tracking and automated alerts
"""
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Alert:
    """Alert configuration and data"""
    id: str
    type: str  # 'profit_drop', 'cost_spike', 'roas_decline', 'campaign_pause'
    title: str
    message: str
    severity: str  # 'critical', 'warning', 'info'
    threshold: float
    current_value: float
    timestamp: datetime
    platform: str
    action_required: bool = False

@dataclass
class DashboardWidget:
    """Dashboard widget configuration"""
    id: str
    type: str  # 'metric', 'chart', 'table', 'alert'
    title: str
    data: Dict[str, Any]
    refresh_interval: int = 300  # seconds
    last_updated: Optional[datetime] = None

class SmartDashboardFeatures:
    """Smart dashboard features with real-time tracking and alerts"""
    
    def __init__(self):
        self.alerts = []
        self.widgets = {}
        self.alert_rules = {}
        self.real_time_data = {}
        self.subscribers = {}  # WebSocket subscribers
        
    def setup_alert_rules(self):
        """Setup default alert rules"""
        self.alert_rules = {
            'profit_drop': {
                'threshold': -20.0,  # 20% drop
                'severity': 'critical',
                'message_template': 'Profit dropped by {percentage}% in {platform}'
            },
            'cost_spike': {
                'threshold': 50.0,  # 50% increase
                'severity': 'warning',
                'message_template': 'Costs increased by {percentage}% in {platform}'
            },
            'roas_decline': {
                'threshold': -30.0,  # 30% decline
                'severity': 'warning',
                'message_template': 'ROAS declined by {percentage}% in {platform}'
            },
            'campaign_pause': {
                'threshold': 0.0,  # Any pause
                'severity': 'info',
                'message_template': 'Campaign {campaign_name} was paused in {platform}'
            }
        }
    
    def check_alerts(self, current_data: Dict[str, Any], previous_data: Dict[str, Any] = None) -> List[Alert]:
        """Check for alert conditions and generate alerts"""
        new_alerts = []
        
        if not previous_data:
            return new_alerts
        
        # Check profit drop
        current_profit = current_data.get('total_profit', 0)
        previous_profit = previous_data.get('total_profit', 0)
        
        if previous_profit > 0:
            profit_change = ((current_profit - previous_profit) / previous_profit) * 100
            if profit_change <= self.alert_rules['profit_drop']['threshold']:
                alert = Alert(
                    id=f"profit_drop_{datetime.now().timestamp()}",
                    type='profit_drop',
                    title='Profit Drop Alert',
                    message=self.alert_rules['profit_drop']['message_template'].format(
                        percentage=abs(profit_change),
                        platform='Overall'
                    ),
                    severity=self.alert_rules['profit_drop']['severity'],
                    threshold=self.alert_rules['profit_drop']['threshold'],
                    current_value=profit_change,
                    timestamp=datetime.now(),
                    platform='Overall',
                    action_required=True
                )
                new_alerts.append(alert)
        
        # Check platform-specific alerts
        for platform in current_data.get('platforms', {}):
            current_platform = current_data['platforms'][platform]
            previous_platform = previous_data.get('platforms', {}).get(platform, {})
            
            if not previous_platform:
                continue
            
            # Check cost spike
            current_cost = current_platform.get('total_costs', 0)
            previous_cost = previous_platform.get('total_costs', 0)
            
            if previous_cost > 0:
                cost_change = ((current_cost - previous_cost) / previous_cost) * 100
                if cost_change >= self.alert_rules['cost_spike']['threshold']:
                    alert = Alert(
                        id=f"cost_spike_{platform}_{datetime.now().timestamp()}",
                        type='cost_spike',
                        title='Cost Spike Alert',
                        message=self.alert_rules['cost_spike']['message_template'].format(
                            percentage=cost_change,
                            platform=platform
                        ),
                        severity=self.alert_rules['cost_spike']['severity'],
                        threshold=self.alert_rules['cost_spike']['threshold'],
                        current_value=cost_change,
                        timestamp=datetime.now(),
                        platform=platform,
                        action_required=True
                    )
                    new_alerts.append(alert)
            
            # Check ROAS decline
            current_roas = current_platform.get('roas', 0)
            previous_roas = previous_platform.get('roas', 0)
            
            if previous_roas > 0:
                roas_change = ((current_roas - previous_roas) / previous_roas) * 100
                if roas_change <= self.alert_rules['roas_decline']['threshold']:
                    alert = Alert(
                        id=f"roas_decline_{platform}_{datetime.now().timestamp()}",
                        type='roas_decline',
                        title='ROAS Decline Alert',
                        message=self.alert_rules['roas_decline']['message_template'].format(
                            percentage=abs(roas_change),
                            platform=platform
                        ),
                        severity=self.alert_rules['roas_decline']['severity'],
                        threshold=self.alert_rules['roas_decline']['threshold'],
                        current_value=roas_change,
                        timestamp=datetime.now(),
                        platform=platform,
                        action_required=True
                    )
                    new_alerts.append(alert)
        
        # Store new alerts
        self.alerts.extend(new_alerts)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
        
        return new_alerts
    
    def create_dashboard_widgets(self, data: Dict[str, Any]) -> Dict[str, DashboardWidget]:
        """Create dashboard widgets from data"""
        widgets = {}
        
        # Profit Overview Widget
        widgets['profit_overview'] = DashboardWidget(
            id='profit_overview',
            type='metric',
            title='Profit Overview',
            data={
                'total_profit': data.get('total_profit', 0),
                'total_revenue': data.get('total_revenue', 0),
                'total_costs': data.get('total_costs', 0),
                'profit_margin': data.get('profit_margin', 0),
                'roas': data.get('roas', 0)
            },
            refresh_interval=300
        )
        
        # Platform Breakdown Widget
        widgets['platform_breakdown'] = DashboardWidget(
            id='platform_breakdown',
            type='chart',
            title='Platform Performance',
            data={
                'platforms': data.get('platform_breakdown', {}),
                'chart_type': 'bar',
                'metrics': ['revenue', 'costs', 'profit']
            },
            refresh_interval=600
        )
        
        # Top Campaigns Widget
        widgets['top_campaigns'] = DashboardWidget(
            id='top_campaigns',
            type='table',
            title='Top Performing Campaigns',
            data={
                'campaigns': self._get_top_campaigns(data),
                'columns': ['name', 'platform', 'revenue', 'costs', 'profit', 'roas']
            },
            refresh_interval=900
        )
        
        # Alerts Widget
        widgets['alerts'] = DashboardWidget(
            id='alerts',
            type='alert',
            title='Recent Alerts',
            data={
                'alerts': self.alerts[-10:],  # Last 10 alerts
                'unread_count': len([a for a in self.alerts if not a.get('read', False)])
            },
            refresh_interval=60
        )
        
        # Cost Efficiency Widget
        widgets['cost_efficiency'] = DashboardWidget(
            id='cost_efficiency',
            type='chart',
            title='Cost Efficiency',
            data={
                'efficiency': data.get('cost_efficiency', {}),
                'chart_type': 'line',
                'metrics': ['cpa', 'cpc', 'cpm']
            },
            refresh_interval=600
        )
        
        self.widgets = widgets
        return widgets
    
    def _get_top_campaigns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get top performing campaigns across all platforms"""
        all_campaigns = []
        
        for platform, platform_data in data.get('platform_breakdown', {}).items():
            campaigns = platform_data.get('campaigns', [])
            for campaign in campaigns:
                campaign['platform'] = platform
                all_campaigns.append(campaign)
        
        # Sort by profit
        all_campaigns.sort(key=lambda x: x.get('profit', 0), reverse=True)
        
        return all_campaigns[:10]  # Top 10
    
    def update_widget_data(self, widget_id: str, new_data: Dict[str, Any]):
        """Update widget data"""
        if widget_id in self.widgets:
            self.widgets[widget_id].data.update(new_data)
            self.widgets[widget_id].last_updated = datetime.now()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get complete dashboard data"""
        return {
            'widgets': {k: {
                'id': v.id,
                'type': v.type,
                'title': v.title,
                'data': v.data,
                'last_updated': v.last_updated.isoformat() if v.last_updated else None
            } for k, v in self.widgets.items()},
            'alerts': [{
                'id': a.id,
                'type': a.type,
                'title': a.title,
                'message': a.message,
                'severity': a.severity,
                'timestamp': a.timestamp.isoformat(),
                'platform': a.platform,
                'action_required': a.action_required
            } for a in self.alerts[-20:]],  # Last 20 alerts
            'last_updated': datetime.now().isoformat()
        }
    
    def export_data(self, format: str = 'json', date_range: Optional[Tuple[datetime, datetime]] = None) -> str:
        """Export dashboard data in specified format"""
        data = self.get_dashboard_data()
        
        if format == 'json':
            return json.dumps(data, indent=2, default=str)
        elif format == 'csv':
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow(['Platform', 'Campaign', 'Revenue', 'Costs', 'Profit', 'ROAS', 'Date'])
            
            # Write data
            for platform, platform_data in data.get('widgets', {}).get('platform_breakdown', {}).get('data', {}).get('platforms', {}).items():
                campaigns = platform_data.get('campaigns', [])
                for campaign in campaigns:
                    writer.writerow([
                        platform,
                        campaign.get('name', ''),
                        campaign.get('revenue', 0),
                        campaign.get('costs', 0),
                        campaign.get('profit', 0),
                        campaign.get('roas', 0),
                        datetime.now().strftime('%Y-%m-%d')
                    ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def setup_real_time_sync(self, sync_interval: int = 300):
        """Setup real-time data synchronization"""
        async def sync_loop():
            while True:
                try:
                    # This would integrate with your data service
                    # For now, we'll just update timestamps
                    for widget in self.widgets.values():
                        widget.last_updated = datetime.now()
                    
                    await asyncio.sleep(sync_interval)
                except Exception as e:
                    logger.error(f"Error in sync loop: {e}")
                    await asyncio.sleep(60)  # Wait 1 minute on error
        
        # Start sync loop
        asyncio.create_task(sync_loop())
    
    def add_alert_rule(self, rule_name: str, threshold: float, severity: str, message_template: str):
        """Add custom alert rule"""
        self.alert_rules[rule_name] = {
            'threshold': threshold,
            'severity': severity,
            'message_template': message_template
        }
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary"""
        total_alerts = len(self.alerts)
        critical_alerts = len([a for a in self.alerts if a.severity == 'critical'])
        warning_alerts = len([a for a in self.alerts if a.severity == 'warning'])
        unread_alerts = len([a for a in self.alerts if not a.get('read', False)])
        
        return {
            'total_alerts': total_alerts,
            'critical_alerts': critical_alerts,
            'warning_alerts': warning_alerts,
            'unread_alerts': unread_alerts,
            'recent_alerts': self.alerts[-5:]  # Last 5 alerts
        }

# Example usage
def main():
    """Example usage of smart dashboard features"""
    dashboard = SmartDashboardFeatures()
    dashboard.setup_alert_rules()
    
    # Sample data
    current_data = {
        'total_profit': 1000,
        'total_revenue': 5000,
        'total_costs': 4000,
        'platforms': {
            'shopify': {'total_costs': 2000, 'roas': 2.5},
            'meta_ads': {'total_costs': 1500, 'roas': 2.0},
            'google_ads': {'total_costs': 500, 'roas': 3.0}
        }
    }
    
    previous_data = {
        'total_profit': 1200,
        'total_revenue': 4800,
        'total_costs': 3600,
        'platforms': {
            'shopify': {'total_costs': 1800, 'roas': 2.7},
            'meta_ads': {'total_costs': 1200, 'roas': 2.2},
            'google_ads': {'total_costs': 600, 'roas': 2.8}
        }
    }
    
    # Check for alerts
    alerts = dashboard.check_alerts(current_data, previous_data)
    print("Alerts:", alerts)
    
    # Create widgets
    widgets = dashboard.create_dashboard_widgets(current_data)
    print("Widgets:", widgets)
    
    # Get dashboard data
    dashboard_data = dashboard.get_dashboard_data()
    print("Dashboard Data:", dashboard_data)
    
    # Export data
    json_export = dashboard.export_data('json')
    print("JSON Export:", json_export[:200] + "...")

if __name__ == "__main__":
    main()
