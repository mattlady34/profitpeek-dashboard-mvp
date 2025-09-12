"""Time period utilities for dashboard queries."""

from datetime import datetime, timedelta
from typing import Dict
import pytz


def get_time_period_dates(period: str, timezone: str = "UTC") -> Dict[datetime, datetime]:
    """Get start and end dates for a time period."""
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if period == "today":
        return {
            "start": today,
            "end": today + timedelta(days=1) - timedelta(microseconds=1)
        }
    elif period == "yesterday":
        yesterday = today - timedelta(days=1)
        return {
            "start": yesterday,
            "end": today - timedelta(microseconds=1)
        }
    elif period == "7d":
        return {
            "start": today - timedelta(days=7),
            "end": today + timedelta(days=1) - timedelta(microseconds=1)
        }
    elif period == "30d":
        return {
            "start": today - timedelta(days=30),
            "end": today + timedelta(days=1) - timedelta(microseconds=1)
        }
    elif period == "mtd":
        month_start = today.replace(day=1)
        return {
            "start": month_start,
            "end": today + timedelta(days=1) - timedelta(microseconds=1)
        }
    elif period == "qtd":
        quarter = (today.month - 1) // 3
        quarter_start = today.replace(month=quarter * 3 + 1, day=1)
        return {
            "start": quarter_start,
            "end": today + timedelta(days=1) - timedelta(microseconds=1)
        }
    elif period == "ytd":
        year_start = today.replace(month=1, day=1)
        return {
            "start": year_start,
            "end": today + timedelta(days=1) - timedelta(microseconds=1)
        }
    else:
        raise ValueError(f"Invalid time period: {period}")
