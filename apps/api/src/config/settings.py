"""Application configuration settings."""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "ProfitPeek API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Database
    database_url: str = Field(..., description="PostgreSQL database URL")
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_pool_timeout: int = 30
    database_pool_recycle: int = 3600
    
    # Redis
    redis_url: str = Field(..., description="Redis URL")
    redis_max_connections: int = 10
    
    # Object Storage (S3/MinIO)
    s3_endpoint: str = Field(..., description="S3 endpoint URL")
    s3_access_key_id: str = Field(..., description="S3 access key ID")
    s3_secret_access_key: str = Field(..., description="S3 secret access key")
    s3_bucket: str = Field(..., description="S3 bucket name")
    s3_region: str = "us-east-1"
    s3_secure: bool = True
    
    # Shopify
    shopify_api_key: str = Field(..., description="Shopify API key")
    shopify_api_secret: str = Field(..., description="Shopify API secret")
    shopify_webhook_secret: str = Field(..., description="Shopify webhook secret")
    shopify_app_url: str = Field(..., description="Shopify app URL")
    shopify_redirect_uri: str = Field(..., description="Shopify OAuth redirect URI")
    shopify_scopes: List[str] = [
        "read_orders",
        "read_products", 
        "read_inventory",
        "read_customers",
        "read_analytics"
    ]
    
    # Email
    smtp_host: str = Field(..., description="SMTP host")
    smtp_port: int = 587
    smtp_user: str = Field(..., description="SMTP username")
    smtp_password: str = Field(..., description="SMTP password")
    smtp_use_tls: bool = True
    from_email: str = Field(..., description="From email address")
    
    # Slack (Optional)
    slack_webhook_url: Optional[str] = Field(None, description="Slack webhook URL")
    
    # Security
    jwt_secret: str = Field(..., description="JWT secret key")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours
    encryption_key: str = Field(..., description="32-byte encryption key")
    
    # Rate Limiting
    rate_limit_requests: int = 1000
    rate_limit_window: int = 60  # seconds
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(None, description="Sentry DSN")
    log_level: str = "INFO"
    
    # Feature Flags
    enable_slack_digest: bool = False
    enable_csv_export: bool = True
    enable_advanced_analytics: bool = False
    enable_multi_currency: bool = True
    enable_llm_digest: bool = False
    
    # Business Logic
    default_fee_percentage: float = 2.9
    default_fee_fixed: float = 0.30
    min_margin_threshold: float = 0.1
    currency_precision: int = 2
    
    # Data Health Thresholds
    missing_costs_warning: float = 0.1
    missing_costs_critical: float = 0.2
    estimated_fees_warning: float = 0.05
    estimated_fees_critical: float = 0.25
    webhook_lag_warning_ms: int = 60000
    webhook_lag_critical_ms: int = 300000
    
    # Backfill
    backfill_days: int = 90
    backfill_batch_size: int = 1000
    backfill_max_retries: int = 3
    
    # Workers
    worker_concurrency: int = 4
    worker_max_retries: int = 3
    worker_retry_delay: int = 60  # seconds
    
    @property
    def database_url_sync(self) -> str:
        """Get synchronous database URL for Alembic."""
        return self.database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    @property
    def redis_config(self) -> dict:
        """Get Redis configuration."""
        return {
            "url": self.redis_url,
            "max_connections": self.redis_max_connections,
            "decode_responses": True,
        }
    
    @property
    def s3_config(self) -> dict:
        """Get S3 configuration."""
        return {
            "endpoint_url": self.s3_endpoint,
            "aws_access_key_id": self.s3_access_key_id,
            "aws_secret_access_key": self.s3_secret_access_key,
            "region_name": self.s3_region,
            "use_ssl": self.s3_secure,
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
