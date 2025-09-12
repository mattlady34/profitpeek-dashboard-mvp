"""Database models for ProfitPeek."""

from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Shop(Base):
    """Shop model for storing Shopify shop information."""
    
    __tablename__ = "shops"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_domain = Column(String(255), unique=True, nullable=False, index=True)
    access_token = Column(Text, nullable=False)  # Encrypted
    timezone = Column(String(50), nullable=False, default="UTC")
    currency = Column(String(3), nullable=False, default="USD")
    email = Column(String(255), nullable=True)
    plan = Column(String(50), nullable=True)
    scopes = Column(ARRAY(String), nullable=False, default=[])
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="shop", cascade="all, delete-orphan")
    settings = relationship("Settings", back_populates="shop", uselist=False, cascade="all, delete-orphan")
    webhook_events = relationship("WebhookEvent", back_populates="shop", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_shops_domain", "shop_domain"),
        Index("idx_shops_created_at", "created_at"),
    )


class Settings(Base):
    """Shop settings for fee presets, shipping costs, etc."""
    
    __tablename__ = "settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    fee_default_pct = Column(Numeric(5, 2), nullable=False, default=2.9)
    fee_overrides = Column(JSONB, nullable=False, default={})
    shipping_cost_rule = Column(JSONB, nullable=False, default={"type": "flat", "value": 0})
    digest_local_time = Column(String(10), nullable=False, default="09:00")
    ad_spend_channels = Column(ARRAY(String), nullable=False, default=[])
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    
    # Relationships
    shop = relationship("Shop", back_populates="settings")
    
    __table_args__ = (
        Index("idx_settings_shop_id", "shop_id"),
    )


class Order(Base):
    """Order model for storing Shopify orders."""
    
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    shop_order_id = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=False)
    currency = Column(String(3), nullable=False)
    presentment_currency = Column(String(3), nullable=False)
    current_total_price = Column(Numeric(10, 2), nullable=False)
    current_total_discounts = Column(Numeric(10, 2), nullable=False, default=0)
    current_total_tax = Column(Numeric(10, 2), nullable=False, default=0)
    current_total_duties = Column(Numeric(10, 2), nullable=True)
    current_total_shipping_price_set = Column(JSONB, nullable=True)
    financial_status = Column(String(50), nullable=False)
    fulfillment_status = Column(String(50), nullable=True)
    customer_id = Column(String(50), nullable=True)
    flags = Column(JSONB, nullable=False, default={})
    created_at_db = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    
    # Relationships
    shop = relationship("Shop", back_populates="orders")
    lines = relationship("OrderLine", back_populates="order", cascade="all, delete-orphan")
    refunds = relationship("RefundLine", back_populates="order", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="order", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("shop_id", "shop_order_id", name="uq_orders_shop_order_id"),
        Index("idx_orders_shop_processed_at", "shop_id", "processed_at"),
        Index("idx_orders_shop_created_at", "shop_id", "created_at"),
        Index("idx_orders_processed_at", "processed_at"),
    )


class OrderLine(Base):
    """Order line items model."""
    
    __tablename__ = "order_lines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    line_id = Column(String(50), nullable=False)
    product_id = Column(String(50), nullable=False)
    variant_id = Column(String(50), nullable=False)
    inventory_item_id = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_set = Column(JSONB, nullable=False)
    discount_allocations = Column(JSONB, nullable=False, default=[])
    presentment_currency = Column(String(3), nullable=False)
    shop_currency = Column(String(3), nullable=False)
    effective_unit_cost = Column(Numeric(10, 2), nullable=True)
    cost_source = Column(Enum("snapshot", "csv", "api", "null", name="cost_source_enum"), nullable=False, default="null")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relationships
    shop = relationship("Shop")
    order = relationship("Order", back_populates="lines")
    
    __table_args__ = (
        Index("idx_order_lines_shop_order", "shop_id", "order_id"),
        Index("idx_order_lines_shop_variant", "shop_id", "variant_id"),
        Index("idx_order_lines_inventory_item", "inventory_item_id"),
    )


class RefundLine(Base):
    """Refund line items model."""
    
    __tablename__ = "refund_lines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    line_id = Column(String(50), nullable=False)
    refunded_quantity = Column(Integer, nullable=False)
    refunded_amount_set = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relationships
    shop = relationship("Shop")
    order = relationship("Order", back_populates="refunds")
    
    __table_args__ = (
        Index("idx_refund_lines_shop_order", "shop_id", "order_id"),
    )


class Transaction(Base):
    """Transaction model for payment transactions."""
    
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    gateway = Column(String(100), nullable=False)
    status = Column(Enum("pending", "failure", "success", "error", name="transaction_status_enum"), nullable=False)
    amount_set = Column(JSONB, nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relationships
    shop = relationship("Shop")
    order = relationship("Order", back_populates="transactions")
    fees = relationship("TransactionFee", back_populates="transaction", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_transactions_shop_order", "shop_id", "order_id"),
    )


class TransactionFee(Base):
    """Transaction fees model."""
    
    __tablename__ = "transaction_fees"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False)
    fee_amount_set = Column(JSONB, nullable=False)
    currency = Column(String(3), nullable=False)
    presentment_currency = Column(String(3), nullable=False)
    estimated = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relationships
    shop = relationship("Shop")
    transaction = relationship("Transaction", back_populates="fees")
    
    __table_args__ = (
        Index("idx_transaction_fees_shop_transaction", "shop_id", "transaction_id"),
    )


class InventoryItemCostSnapshot(Base):
    """Inventory item cost snapshots for historical tracking."""
    
    __tablename__ = "inventory_item_cost_snapshots"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    inventory_item_id = Column(String(50), nullable=False)
    effective_date = Column(DateTime(timezone=True), nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    source = Column(Enum("api", "csv", name="cost_source_enum"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relationships
    shop = relationship("Shop")
    
    __table_args__ = (
        UniqueConstraint("shop_id", "inventory_item_id", "effective_date", name="uq_cost_snapshots_item_date"),
        Index("idx_cost_snapshots_shop_item", "shop_id", "inventory_item_id"),
        Index("idx_cost_snapshots_effective_date", "effective_date"),
    )


class DailyRollup(Base):
    """Daily aggregated metrics rollup."""
    
    __tablename__ = "rollups_daily"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    net_revenue = Column(Numeric(12, 2), nullable=False, default=0)
    cogs = Column(Numeric(12, 2), nullable=False, default=0)
    fees = Column(Numeric(12, 2), nullable=False, default=0)
    shipping_cost = Column(Numeric(12, 2), nullable=False, default=0)
    ad_spend = Column(JSONB, nullable=False, default={})
    net_profit = Column(Numeric(12, 2), nullable=False, default=0)
    margin_pct = Column(Numeric(5, 2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    
    # Relationships
    shop = relationship("Shop")
    
    __table_args__ = (
        UniqueConstraint("shop_id", "date", name="uq_rollups_daily_shop_date"),
        Index("idx_rollups_daily_shop_date", "shop_id", "date"),
    )


class AdSpendDaily(Base):
    """Daily ad spend tracking."""
    
    __tablename__ = "ad_spend_daily"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    channel = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relationships
    shop = relationship("Shop")
    
    __table_args__ = (
        Index("idx_ad_spend_daily_shop_date_channel", "shop_id", "date", "channel"),
    )


class WebhookEvent(Base):
    """Webhook events tracking."""
    
    __tablename__ = "webhook_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    shop_id = Column(UUID(as_uuid=True), ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    topic = Column(String(100), nullable=False)
    shop_resource_id = Column(String(50), nullable=False)
    received_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    dedup_key = Column(String(255), unique=True, nullable=False)
    status = Column(Enum("pending", "processing", "completed", "failed", name="webhook_status_enum"), nullable=False, default="pending")
    error = Column(Text, nullable=True)
    
    # Relationships
    shop = relationship("Shop", back_populates="webhook_events")
    
    __table_args__ = (
        Index("idx_webhook_events_shop_status", "shop_id", "status"),
        Index("idx_webhook_events_dedup_key", "dedup_key"),
        Index("idx_webhook_events_received_at", "received_at"),
    )
