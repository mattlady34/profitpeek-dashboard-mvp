"""
Real-time Profit Tracking Dashboard with live updates and monitoring
"""
import asyncio
import websockets
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
import logging
import threading
import time

logger = logging.getLogger(__name__)

@dataclass
class ProfitSnapshot:
    """Real-time profit snapshot"""
    timestamp: datetime
    total_profit: float
    total_revenue: float
    total_costs: float
    profit_margin: float
    roas: float
    platform_breakdown: Dict[str, Dict[str, float]]
    alerts: List[Dict[str, Any]]
    trends: Dict[str, Any]

@dataclass
class LiveMetric:
    """Live metric for real-time updates"""
    name: str
    value: float
    change: float
    change_percentage: float
    trend: str  # 'up', 'down', 'stable'
    timestamp: datetime

class RealTimeProfitTracker:
    """Real-time profit tracking with live updates"""
    
    def __init__(self):
        self.connected_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.profit_history: List[ProfitSnapshot] = []
        self.live_metrics: Dict[str, LiveMetric] = {}
        self.update_interval = 30  # seconds
        self.is_running = False
        self.data_service = None
        self.alert_thresholds = {
            'profit_drop': -20.0,  # 20% drop
            'cost_spike': 50.0,    # 50% increase
            'roas_decline': -30.0  # 30% decline
        }
    
    def set_data_service(self, data_service):
        """Set the data integration service"""
        self.data_service = data_service
    
    async def start_tracking(self):
        """Start real-time profit tracking"""
        self.is_running = True
        logger.info("Starting real-time profit tracking...")
        
        # Start background update task
        asyncio.create_task(self._update_loop())
        
        # Start WebSocket server
        await self._start_websocket_server()
    
    async def stop_tracking(self):
        """Stop real-time profit tracking"""
        self.is_running = False
        logger.info("Stopping real-time profit tracking...")
        
        # Close all WebSocket connections
        for client in self.connected_clients.copy():
            await client.close()
    
    async def _update_loop(self):
        """Background update loop"""
        while self.is_running:
            try:
                # Get latest data from data service
                if self.data_service:
                    await self._update_profit_data()
                
                # Update live metrics
                self._update_live_metrics()
                
                # Check for alerts
                alerts = self._check_alerts()
                
                # Broadcast updates to connected clients
                await self._broadcast_updates()
                
                # Wait for next update
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Error in update loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _update_profit_data(self):
        """Update profit data from data service"""
        try:
            # Get current data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1)
            
            # Sync all platforms
            sync_results = await self.data_service.sync_all_platforms(start_date, end_date)
            
            # Calculate profit metrics
            profit_metrics = self._calculate_profit_metrics(sync_results)
            
            # Create profit snapshot
            snapshot = ProfitSnapshot(
                timestamp=datetime.now(),
                total_profit=profit_metrics['total_profit'],
                total_revenue=profit_metrics['total_revenue'],
                total_costs=profit_metrics['total_costs'],
                profit_margin=profit_metrics['profit_margin'],
                roas=profit_metrics['roas'],
                platform_breakdown=profit_metrics['platform_breakdown'],
                alerts=[],
                trends=profit_metrics['trends']
            )
            
            # Store snapshot
            self.profit_history.append(snapshot)
            
            # Keep only last 1000 snapshots
            if len(self.profit_history) > 1000:
                self.profit_history = self.profit_history[-1000:]
            
            logger.info(f"Profit data updated: ${snapshot.total_profit:.2f}")
            
        except Exception as e:
            logger.error(f"Error updating profit data: {e}")
    
    def _calculate_profit_metrics(self, sync_results: List[Any]) -> Dict[str, Any]:
        """Calculate profit metrics from sync results"""
        total_profit = 0.0
        total_revenue = 0.0
        total_costs = 0.0
        platform_breakdown = {}
        
        for result in sync_results:
            if result.success:
                platform = result.platform
                # This would integrate with your actual data calculation
                # For now, using mock data
                platform_profit = 1000.0  # Mock value
                platform_revenue = 5000.0  # Mock value
                platform_costs = 4000.0  # Mock value
                
                total_profit += platform_profit
                total_revenue += platform_revenue
                total_costs += platform_costs
                
                platform_breakdown[platform] = {
                    'profit': platform_profit,
                    'revenue': platform_revenue,
                    'costs': platform_costs,
                    'roas': platform_revenue / platform_costs if platform_costs > 0 else 0
                }
        
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        roas = total_revenue / total_costs if total_costs > 0 else 0
        
        return {
            'total_profit': total_profit,
            'total_revenue': total_revenue,
            'total_costs': total_costs,
            'profit_margin': profit_margin,
            'roas': roas,
            'platform_breakdown': platform_breakdown,
            'trends': self._calculate_trends()
        }
    
    def _calculate_trends(self) -> Dict[str, Any]:
        """Calculate trends from profit history"""
        if len(self.profit_history) < 2:
            return {}
        
        recent_snapshots = self.profit_history[-10:]  # Last 10 snapshots
        
        # Calculate profit trend
        profit_values = [s.total_profit for s in recent_snapshots]
        profit_trend = self._calculate_trend_direction(profit_values)
        
        # Calculate revenue trend
        revenue_values = [s.total_revenue for s in recent_snapshots]
        revenue_trend = self._calculate_trend_direction(revenue_values)
        
        # Calculate ROAS trend
        roas_values = [s.roas for s in recent_snapshots]
        roas_trend = self._calculate_trend_direction(roas_values)
        
        return {
            'profit_trend': profit_trend,
            'revenue_trend': revenue_trend,
            'roas_trend': roas_trend
        }
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate trend direction for a list of values"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear trend
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        change_percentage = ((second_avg - first_avg) / first_avg * 100) if first_avg != 0 else 0
        
        if change_percentage > 5:
            return 'up'
        elif change_percentage < -5:
            return 'down'
        else:
            return 'stable'
    
    def _update_live_metrics(self):
        """Update live metrics"""
        if not self.profit_history:
            return
        
        latest = self.profit_history[-1]
        previous = self.profit_history[-2] if len(self.profit_history) > 1 else latest
        
        # Update profit metric
        profit_change = latest.total_profit - previous.total_profit
        profit_change_pct = (profit_change / previous.total_profit * 100) if previous.total_profit != 0 else 0
        
        self.live_metrics['profit'] = LiveMetric(
            name='Total Profit',
            value=latest.total_profit,
            change=profit_change,
            change_percentage=profit_change_pct,
            trend='up' if profit_change > 0 else 'down' if profit_change < 0 else 'stable',
            timestamp=latest.timestamp
        )
        
        # Update revenue metric
        revenue_change = latest.total_revenue - previous.total_revenue
        revenue_change_pct = (revenue_change / previous.total_revenue * 100) if previous.total_revenue != 0 else 0
        
        self.live_metrics['revenue'] = LiveMetric(
            name='Total Revenue',
            value=latest.total_revenue,
            change=revenue_change,
            change_percentage=revenue_change_pct,
            trend='up' if revenue_change > 0 else 'down' if revenue_change < 0 else 'stable',
            timestamp=latest.timestamp
        )
        
        # Update ROAS metric
        roas_change = latest.roas - previous.roas
        roas_change_pct = (roas_change / previous.roas * 100) if previous.roas != 0 else 0
        
        self.live_metrics['roas'] = LiveMetric(
            name='ROAS',
            value=latest.roas,
            change=roas_change,
            change_percentage=roas_change_pct,
            trend='up' if roas_change > 0 else 'down' if roas_change < 0 else 'stable',
            timestamp=latest.timestamp
        )
    
    def _check_alerts(self) -> List[Dict[str, Any]]:
        """Check for alert conditions"""
        alerts = []
        
        if len(self.profit_history) < 2:
            return alerts
        
        latest = self.profit_history[-1]
        previous = self.profit_history[-2]
        
        # Check profit drop
        if previous.total_profit > 0:
            profit_change_pct = ((latest.total_profit - previous.total_profit) / previous.total_profit * 100)
            if profit_change_pct <= self.alert_thresholds['profit_drop']:
                alerts.append({
                    'type': 'profit_drop',
                    'severity': 'critical',
                    'message': f'Profit dropped by {abs(profit_change_pct):.1f}%',
                    'timestamp': latest.timestamp.isoformat()
                })
        
        # Check cost spike
        if previous.total_costs > 0:
            cost_change_pct = ((latest.total_costs - previous.total_costs) / previous.total_costs * 100)
            if cost_change_pct >= self.alert_thresholds['cost_spike']:
                alerts.append({
                    'type': 'cost_spike',
                    'severity': 'warning',
                    'message': f'Costs increased by {cost_change_pct:.1f}%',
                    'timestamp': latest.timestamp.isoformat()
                })
        
        # Check ROAS decline
        if previous.roas > 0:
            roas_change_pct = ((latest.roas - previous.roas) / previous.roas * 100)
            if roas_change_pct <= self.alert_thresholds['roas_decline']:
                alerts.append({
                    'type': 'roas_decline',
                    'severity': 'warning',
                    'message': f'ROAS declined by {abs(roas_change_pct):.1f}%',
                    'timestamp': latest.timestamp.isoformat()
                })
        
        return alerts
    
    async def _broadcast_updates(self):
        """Broadcast updates to all connected clients"""
        if not self.connected_clients:
            return
        
        try:
            # Prepare update data
            update_data = {
                'type': 'profit_update',
                'timestamp': datetime.now().isoformat(),
                'snapshot': asdict(self.profit_history[-1]) if self.profit_history else None,
                'live_metrics': {k: asdict(v) for k, v in self.live_metrics.items()},
                'alerts': self._check_alerts()
            }
            
            # Broadcast to all clients
            message = json.dumps(update_data, default=str)
            disconnected_clients = set()
            
            for client in self.connected_clients:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.add(client)
                except Exception as e:
                    logger.error(f"Error sending update to client: {e}")
                    disconnected_clients.add(client)
            
            # Remove disconnected clients
            self.connected_clients -= disconnected_clients
            
        except Exception as e:
            logger.error(f"Error broadcasting updates: {e}")
    
    async def _start_websocket_server(self):
        """Start WebSocket server for real-time updates"""
        async def handle_client(websocket, path):
            """Handle WebSocket client connection"""
            self.connected_clients.add(websocket)
            logger.info(f"Client connected. Total clients: {len(self.connected_clients)}")
            
            try:
                # Send initial data
                if self.profit_history:
                    initial_data = {
                        'type': 'initial_data',
                        'snapshot': asdict(self.profit_history[-1]),
                        'live_metrics': {k: asdict(v) for k, v in self.live_metrics.items()}
                    }
                    await websocket.send(json.dumps(initial_data, default=str))
                
                # Keep connection alive
                async for message in websocket:
                    # Handle client messages if needed
                    pass
                    
            except websockets.exceptions.ConnectionClosed:
                pass
            finally:
                self.connected_clients.discard(websocket)
                logger.info(f"Client disconnected. Total clients: {len(self.connected_clients)}")
        
        # Start WebSocket server
        start_server = websockets.serve(handle_client, "localhost", 8765)
        await start_server
        logger.info("WebSocket server started on ws://localhost:8765")
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current profit tracking status"""
        return {
            'is_running': self.is_running,
            'connected_clients': len(self.connected_clients),
            'snapshots_count': len(self.profit_history),
            'last_update': self.profit_history[-1].timestamp.isoformat() if self.profit_history else None,
            'live_metrics': {k: asdict(v) for k, v in self.live_metrics.items()},
            'alert_thresholds': self.alert_thresholds
        }
    
    def get_profit_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get profit history for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_snapshots = [s for s in self.profit_history if s.timestamp > cutoff_time]
        return [asdict(s) for s in recent_snapshots]
    
    def get_platform_performance(self) -> Dict[str, Any]:
        """Get platform performance summary"""
        if not self.profit_history:
            return {}
        
        latest = self.profit_history[-1]
        return {
            'platforms': latest.platform_breakdown,
            'total_profit': latest.total_profit,
            'total_revenue': latest.total_revenue,
            'total_costs': latest.total_costs,
            'profit_margin': latest.profit_margin,
            'roas': latest.roas,
            'timestamp': latest.timestamp.isoformat()
        }

# Example usage
async def main():
    """Example usage of real-time profit tracker"""
    tracker = RealTimeProfitTracker()
    
    # Start tracking
    await tracker.start_tracking()
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await tracker.stop_tracking()

if __name__ == "__main__":
    asyncio.run(main())
