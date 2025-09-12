"""Deduplication utilities for webhooks and events."""

import hashlib
from typing import Any, Dict
from datetime import datetime


def generate_dedup_key(
    topic: str, 
    shop_domain: str, 
    resource_id: str, 
    timestamp: str
) -> str:
    """Generate a unique deduplication key for webhook events."""
    key_data = f"{topic}:{shop_domain}:{resource_id}:{timestamp}"
    return hashlib.sha256(key_data.encode()).hexdigest()


def generate_webhook_dedup_key(
    topic: str, 
    shop_domain: str, 
    resource_id: str, 
    timestamp: str
) -> str:
    """Generate deduplication key specifically for webhook events."""
    return generate_dedup_key(topic, shop_domain, resource_id, timestamp)


def generate_bulk_operation_key(
    operation_type: str, 
    shop_id: str, 
    date_range: str
) -> str:
    """Generate deduplication key for bulk operations."""
    key_data = f"bulk:{operation_type}:{shop_id}:{date_range}"
    return hashlib.sha256(key_data.encode()).hexdigest()


def is_duplicate_event(
    existing_events: list, 
    new_event: Dict[str, Any]
) -> bool:
    """Check if an event is a duplicate based on existing events."""
    new_dedup_key = new_event.get('dedup_key')
    if not new_dedup_key:
        return False
    
    for existing_event in existing_events:
        if existing_event.get('dedup_key') == new_dedup_key:
            return True
    
    return False


def create_event_fingerprint(event_data: Dict[str, Any]) -> str:
    """Create a fingerprint for event data to detect duplicates."""
    # Create a stable representation of the event data
    fingerprint_data = {
        'id': event_data.get('id'),
        'created_at': event_data.get('created_at'),
        'updated_at': event_data.get('updated_at'),
    }
    
    # Convert to string and hash
    fingerprint_str = str(sorted(fingerprint_data.items()))
    return hashlib.md5(fingerprint_str.encode()).hexdigest()
