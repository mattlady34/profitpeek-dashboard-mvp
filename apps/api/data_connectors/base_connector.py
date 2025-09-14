"""
Base connector class for all data integrations
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BaseConnector(ABC):
    """Base class for all data connectors"""
    
    def __init__(self, api_key: str, api_secret: str = None, base_url: str = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(self._get_default_headers())
    
    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for API requests"""
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'ProfitPeek/1.0'
        }
    
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the API"""
        pass
    
    @abstractmethod
    def get_orders(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get orders data from the platform"""
        pass
    
    @abstractmethod
    def get_campaigns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get campaigns data from the platform"""
        pass
    
    @abstractmethod
    def get_products(self) -> List[Dict[str, Any]]:
        """Get products data from the platform"""
        pass
    
    def make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            return self.authenticate()
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
