"""
Enhanced Data Integration Service with advanced features
"""
import asyncio
import aiohttp
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SyncResult:
    """Result of a data synchronization operation"""
    platform: str
    success: bool
    data_count: int
    error: Optional[str] = None
    sync_time: float = 0.0

class EnhancedDataIntegrationService:
    """Enhanced data integration service with advanced features"""
    
    def __init__(self):
        self.connectors = {}
        self.sync_history = []
        self.health_status = {}
        self.retry_config = {
            'max_retries': 3,
            'base_delay': 1.0,
            'max_delay': 60.0,
            'backoff_factor': 2.0
        }
    
    def add_connector(self, platform: str, connector):
        """Add a connector for a platform"""
        self.connectors[platform] = connector
        self.health_status[platform] = {
            'status': 'unknown',
            'last_sync': None,
            'error_count': 0,
            'success_rate': 0.0
        }
    
    async def test_all_connections(self) -> Dict[str, bool]:
        """Test connections to all platforms"""
        results = {}
        
        for platform, connector in self.connectors.items():
            try:
                if hasattr(connector, 'test_connection'):
                    success = await self._test_connection_with_retry(connector)
                    results[platform] = success
                    self.health_status[platform]['status'] = 'healthy' if success else 'unhealthy'
                else:
                    results[platform] = False
                    self.health_status[platform]['status'] = 'no_test_method'
            except Exception as e:
                logger.error(f"Error testing {platform} connection: {e}")
                results[platform] = False
                self.health_status[platform]['status'] = 'error'
        
        return results
    
    async def _test_connection_with_retry(self, connector) -> bool:
        """Test connection with retry logic"""
        for attempt in range(self.retry_config['max_retries']):
            try:
                if asyncio.iscoroutinefunction(connector.test_connection):
                    return await connector.test_connection()
                else:
                    return connector.test_connection()
            except Exception as e:
                if attempt < self.retry_config['max_retries'] - 1:
                    delay = min(
                        self.retry_config['base_delay'] * (self.retry_config['backoff_factor'] ** attempt),
                        self.retry_config['max_delay']
                    )
                    logger.warning(f"Connection test failed, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Connection test failed after {self.retry_config['max_retries']} attempts: {e}")
                    return False
        return False
    
    async def sync_all_platforms(self, start_date: datetime, end_date: datetime) -> List[SyncResult]:
        """Sync data from all platforms with advanced error handling"""
        results = []
        
        # Test all connections first
        connection_status = await self.test_all_connections()
        
        for platform, connector in self.connectors.items():
            if not connection_status.get(platform, False):
                results.append(SyncResult(
                    platform=platform,
                    success=False,
                    data_count=0,
                    error="Connection test failed"
                ))
                continue
            
            # Sync this platform
            result = await self._sync_platform_with_retry(platform, connector, start_date, end_date)
            results.append(result)
            
            # Update health status
            self._update_health_status(platform, result)
        
        # Store sync history
        self.sync_history.append({
            'timestamp': datetime.now(),
            'results': results,
            'total_platforms': len(self.connectors),
            'successful_platforms': sum(1 for r in results if r.success)
        })
        
        return results
    
    async def _sync_platform_with_retry(self, platform: str, connector, start_date: datetime, end_date: datetime) -> SyncResult:
        """Sync a single platform with retry logic"""
        start_time = time.time()
        
        for attempt in range(self.retry_config['max_retries']):
            try:
                # Get data from platform
                if hasattr(connector, 'get_campaigns'):
                    campaigns = await self._get_campaigns_async(connector, start_date, end_date)
                    data_count = len(campaigns)
                else:
                    data_count = 0
                
                sync_time = time.time() - start_time
                
                return SyncResult(
                    platform=platform,
                    success=True,
                    data_count=data_count,
                    sync_time=sync_time
                )
                
            except Exception as e:
                if attempt < self.retry_config['max_retries'] - 1:
                    delay = min(
                        self.retry_config['base_delay'] * (self.retry_config['backoff_factor'] ** attempt),
                        self.retry_config['max_delay']
                    )
                    logger.warning(f"Sync failed for {platform}, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Sync failed for {platform} after {self.retry_config['max_retries']} attempts: {e}")
                    return SyncResult(
                        platform=platform,
                        success=False,
                        data_count=0,
                        error=str(e),
                        sync_time=time.time() - start_time
                    )
        
        return SyncResult(
            platform=platform,
            success=False,
            data_count=0,
            error="Max retries exceeded",
            sync_time=time.time() - start_time
        )
    
    async def _get_campaigns_async(self, connector, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get campaigns asynchronously"""
        if asyncio.iscoroutinefunction(connector.get_campaigns):
            return await connector.get_campaigns(start_date, end_date)
        else:
            # Run in thread pool for sync methods
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, connector.get_campaigns, start_date, end_date)
    
    def _update_health_status(self, platform: str, result: SyncResult):
        """Update health status for a platform"""
        if result.success:
            self.health_status[platform]['error_count'] = 0
            self.health_status[platform]['last_sync'] = datetime.now()
        else:
            self.health_status[platform]['error_count'] += 1
        
        # Calculate success rate
        total_syncs = len([h for h in self.sync_history if h['timestamp'] > datetime.now() - timedelta(days=7)])
        successful_syncs = len([h for h in self.sync_history if h['timestamp'] > datetime.now() - timedelta(days=7) and h['successful_platforms'] > 0])
        self.health_status[platform]['success_rate'] = successful_syncs / total_syncs if total_syncs > 0 else 0.0
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of all platforms"""
        return {
            'platforms': self.health_status,
            'overall_health': self._calculate_overall_health(),
            'last_sync': self.sync_history[-1]['timestamp'] if self.sync_history else None
        }
    
    def _calculate_overall_health(self) -> str:
        """Calculate overall health status"""
        if not self.health_status:
            return 'unknown'
        
        healthy_platforms = sum(1 for status in self.health_status.values() if status['status'] == 'healthy')
        total_platforms = len(self.health_status)
        
        if healthy_platforms == total_platforms:
            return 'healthy'
        elif healthy_platforms > total_platforms // 2:
            return 'degraded'
        else:
            return 'unhealthy'
    
    def get_sync_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get sync history for the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [h for h in self.sync_history if h['timestamp'] > cutoff_date]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        if not self.sync_history:
            return {}
        
        recent_history = self.get_sync_history(7)
        
        total_syncs = len(recent_history)
        successful_syncs = sum(1 for h in recent_history if h['successful_platforms'] > 0)
        avg_sync_time = sum(h['results'][0].sync_time for h in recent_history if h['results']) / total_syncs if total_syncs > 0 else 0
        
        return {
            'total_syncs': total_syncs,
            'successful_syncs': successful_syncs,
            'success_rate': successful_syncs / total_syncs if total_syncs > 0 else 0,
            'avg_sync_time': avg_sync_time,
            'platforms_connected': len(self.connectors)
        }

# Example usage
async def main():
    """Example usage of enhanced data service"""
    service = EnhancedDataIntegrationService()
    
    # Add connectors (you'll add these when you get API keys)
    # service.add_connector('shopify', shopify_connector)
    # service.add_connector('meta_ads', meta_ads_connector)
    # service.add_connector('google_ads', google_ads_connector)
    # service.add_connector('klaviyo', klaviyo_connector)
    # service.add_connector('postscript', postscript_connector)
    
    # Test connections
    connection_status = await service.test_all_connections()
    print("Connection Status:", connection_status)
    
    # Sync all platforms
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    results = await service.sync_all_platforms(start_date, end_date)
    print("Sync Results:", results)
    
    # Get health status
    health = service.get_health_status()
    print("Health Status:", health)
    
    # Get performance metrics
    metrics = service.get_performance_metrics()
    print("Performance Metrics:", metrics)

if __name__ == "__main__":
    asyncio.run(main())
