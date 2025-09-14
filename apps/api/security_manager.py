"""
Security Manager for API key encryption, environment management, and production security
"""
import os
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class SecurityManager:
    """Security manager for API keys and sensitive data"""
    
    def __init__(self, master_key: Optional[str] = None):
        self.master_key = master_key or self._generate_master_key()
        self.cipher = Fernet(self.master_key.encode())
        self.encrypted_keys = {}
        self.key_metadata = {}
    
    def _generate_master_key(self) -> str:
        """Generate a master key for encryption"""
        return Fernet.generate_key().decode()
    
    def encrypt_api_key(self, platform: str, api_key: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Encrypt an API key"""
        try:
            # Encrypt the API key
            encrypted_key = self.cipher.encrypt(api_key.encode())
            encrypted_b64 = base64.b64encode(encrypted_key).decode()
            
            # Store encrypted key and metadata
            self.encrypted_keys[platform] = encrypted_b64
            self.key_metadata[platform] = {
                'encrypted_at': datetime.now().isoformat(),
                'platform': platform,
                'metadata': metadata or {}
            }
            
            logger.info(f"API key encrypted for platform: {platform}")
            return encrypted_b64
            
        except Exception as e:
            logger.error(f"Error encrypting API key for {platform}: {e}")
            raise
    
    def decrypt_api_key(self, platform: str) -> Optional[str]:
        """Decrypt an API key"""
        try:
            if platform not in self.encrypted_keys:
                logger.warning(f"No encrypted key found for platform: {platform}")
                return None
            
            # Decrypt the API key
            encrypted_b64 = self.encrypted_keys[platform]
            encrypted_key = base64.b64decode(encrypted_b64.encode())
            decrypted_key = self.cipher.decrypt(encrypted_key).decode()
            
            logger.info(f"API key decrypted for platform: {platform}")
            return decrypted_key
            
        except Exception as e:
            logger.error(f"Error decrypting API key for {platform}: {e}")
            return None
    
    def store_encrypted_keys(self, file_path: str = "encrypted_keys.json"):
        """Store encrypted keys to file"""
        try:
            data = {
                'encrypted_keys': self.encrypted_keys,
                'key_metadata': self.key_metadata,
                'stored_at': datetime.now().isoformat()
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Encrypted keys stored to: {file_path}")
            
        except Exception as e:
            logger.error(f"Error storing encrypted keys: {e}")
            raise
    
    def load_encrypted_keys(self, file_path: str = "encrypted_keys.json"):
        """Load encrypted keys from file"""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"Encrypted keys file not found: {file_path}")
                return
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.encrypted_keys = data.get('encrypted_keys', {})
            self.key_metadata = data.get('key_metadata', {})
            
            logger.info(f"Encrypted keys loaded from: {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading encrypted keys: {e}")
            raise
    
    def get_key_metadata(self, platform: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a platform's API key"""
        return self.key_metadata.get(platform)
    
    def list_encrypted_platforms(self) -> List[str]:
        """List all platforms with encrypted keys"""
        return list(self.encrypted_keys.keys())
    
    def rotate_api_key(self, platform: str, new_api_key: str) -> bool:
        """Rotate an API key"""
        try:
            # Encrypt new key
            self.encrypt_api_key(platform, new_api_key)
            
            # Update metadata
            if platform in self.key_metadata:
                self.key_metadata[platform]['rotated_at'] = datetime.now().isoformat()
                self.key_metadata[platform]['rotation_count'] = self.key_metadata[platform].get('rotation_count', 0) + 1
            
            logger.info(f"API key rotated for platform: {platform}")
            return True
            
        except Exception as e:
            logger.error(f"Error rotating API key for {platform}: {e}")
            return False
    
    def validate_api_key(self, platform: str, api_key: str) -> bool:
        """Validate an API key format"""
        validation_rules = {
            'shopify': {
                'min_length': 20,
                'pattern': r'^[a-f0-9]{32}$'  # Shopify API keys are 32 hex chars
            },
            'meta_ads': {
                'min_length': 50,
                'pattern': r'^[A-Za-z0-9_-]+$'  # Facebook access tokens
            },
            'google_ads': {
                'min_length': 100,
                'pattern': r'^[A-Za-z0-9._-]+$'  # Google OAuth tokens
            },
            'klaviyo': {
                'min_length': 20,
                'pattern': r'^pk_[a-f0-9]{32}$'  # Klaviyo API keys
            },
            'postscript': {
                'min_length': 20,
                'pattern': r'^[A-Za-z0-9_-]+$'  # Postscript API keys
            }
        }
        
        if platform not in validation_rules:
            return True  # Unknown platform, assume valid
        
        rules = validation_rules[platform]
        
        # Check length
        if len(api_key) < rules['min_length']:
            return False
        
        # Check pattern (basic regex check)
        import re
        if not re.match(rules['pattern'], api_key):
            return False
        
        return True
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(length)
    
    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data for logging"""
        return hashlib.sha256(data.encode()).hexdigest()[:8]
    
    def sanitize_log_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data for logging by hashing sensitive fields"""
        sensitive_fields = ['api_key', 'access_token', 'client_secret', 'password']
        sanitized = data.copy()
        
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = f"<HASHED:{self.hash_sensitive_data(str(sanitized[field]))}>"
        
        return sanitized

class EnvironmentManager:
    """Environment variable manager for production deployment"""
    
    def __init__(self):
        self.required_vars = [
            'SHOPIFY_API_KEY',
            'SHOPIFY_API_SECRET',
            'META_ADS_ACCESS_TOKEN',
            'META_ADS_ACCOUNT_ID',
            'GOOGLE_ADS_ACCESS_TOKEN',
            'GOOGLE_ADS_CUSTOMER_ID',
            'GOOGLE_ADS_DEVELOPER_TOKEN',
            'KLAVIYO_API_KEY',
            'POSTSCRIPT_API_KEY',
            'JWT_SECRET',
            'DATABASE_URL'
        ]
        
        self.optional_vars = [
            'REDIS_URL',
            'SENTRY_DSN',
            'LOG_LEVEL',
            'ENVIRONMENT'
        ]
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validate environment variables"""
        results = {
            'valid': True,
            'missing_required': [],
            'missing_optional': [],
            'invalid_values': []
        }
        
        # Check required variables
        for var in self.required_vars:
            if not os.getenv(var):
                results['missing_required'].append(var)
                results['valid'] = False
        
        # Check optional variables
        for var in self.optional_vars:
            if not os.getenv(var):
                results['missing_optional'].append(var)
        
        # Validate specific values
        if os.getenv('LOG_LEVEL') and os.getenv('LOG_LEVEL') not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            results['invalid_values'].append('LOG_LEVEL')
            results['valid'] = False
        
        if os.getenv('ENVIRONMENT') and os.getenv('ENVIRONMENT') not in ['development', 'staging', 'production']:
            results['invalid_values'].append('ENVIRONMENT')
            results['valid'] = False
        
        return results
    
    def get_environment_summary(self) -> Dict[str, Any]:
        """Get environment configuration summary"""
        return {
            'environment': os.getenv('ENVIRONMENT', 'development'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'required_vars_loaded': len([v for v in self.required_vars if os.getenv(v)]),
            'total_required_vars': len(self.required_vars),
            'optional_vars_loaded': len([v for v in self.optional_vars if os.getenv(v)]),
            'total_optional_vars': len(self.optional_vars)
        }
    
    def create_env_template(self, file_path: str = ".env.template"):
        """Create environment template file"""
        template_content = "# ProfitPeek Environment Variables\n\n"
        
        template_content += "# Required Variables\n"
        for var in self.required_vars:
            template_content += f"{var}=your_{var.lower()}_here\n"
        
        template_content += "\n# Optional Variables\n"
        for var in self.optional_vars:
            template_content += f"# {var}=your_{var.lower()}_here\n"
        
        template_content += "\n# Security\n"
        template_content += "JWT_SECRET=your_jwt_secret_here\n"
        template_content += "ENCRYPTION_KEY=your_encryption_key_here\n"
        
        try:
            with open(file_path, 'w') as f:
                f.write(template_content)
            
            logger.info(f"Environment template created: {file_path}")
            
        except Exception as e:
            logger.error(f"Error creating environment template: {e}")
            raise

class ProductionSecurity:
    """Production security features"""
    
    def __init__(self):
        self.rate_limits = {}
        self.blocked_ips = set()
        self.suspicious_activities = []
    
    def check_rate_limit(self, ip: str, endpoint: str, limit: int = 100, window: int = 3600) -> bool:
        """Check if IP is within rate limit"""
        key = f"{ip}:{endpoint}"
        now = datetime.now()
        
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        # Remove old entries
        self.rate_limits[key] = [
            timestamp for timestamp in self.rate_limits[key]
            if (now - timestamp).total_seconds() < window
        ]
        
        # Check if limit exceeded
        if len(self.rate_limits[key]) >= limit:
            return False
        
        # Add current request
        self.rate_limits[key].append(now)
        return True
    
    def block_ip(self, ip: str, reason: str = "Suspicious activity"):
        """Block an IP address"""
        self.blocked_ips.add(ip)
        logger.warning(f"IP blocked: {ip} - {reason}")
    
    def is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is blocked"""
        return ip in self.blocked_ips
    
    def log_suspicious_activity(self, ip: str, activity: str, details: Dict[str, Any]):
        """Log suspicious activity"""
        self.suspicious_activities.append({
            'ip': ip,
            'activity': activity,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 1000 activities
        if len(self.suspicious_activities) > 1000:
            self.suspicious_activities = self.suspicious_activities[-1000:]
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security summary"""
        return {
            'blocked_ips': len(self.blocked_ips),
            'suspicious_activities': len(self.suspicious_activities),
            'rate_limited_endpoints': len(self.rate_limits),
            'recent_activities': self.suspicious_activities[-10:]  # Last 10 activities
        }

# Example usage
def main():
    """Example usage of security manager"""
    # Security Manager
    security = SecurityManager()
    
    # Encrypt API keys
    security.encrypt_api_key('shopify', 'your_shopify_api_key_here')
    security.encrypt_api_key('meta_ads', 'your_meta_ads_token_here')
    
    # Store encrypted keys
    security.store_encrypted_keys()
    
    # Environment Manager
    env_manager = EnvironmentManager()
    env_status = env_manager.validate_environment()
    print("Environment Status:", env_status)
    
    # Create environment template
    env_manager.create_env_template()
    
    # Production Security
    prod_security = ProductionSecurity()
    
    # Check rate limit
    is_allowed = prod_security.check_rate_limit('192.168.1.1', '/api/dashboard')
    print("Rate limit check:", is_allowed)
    
    # Get security summary
    security_summary = prod_security.get_security_summary()
    print("Security Summary:", security_summary)

if __name__ == "__main__":
    main()
