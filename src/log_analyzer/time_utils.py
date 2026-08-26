"""Shared timestamp parsing utilities for Log Analyzer."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional


TIMESTAMP_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S.%f%z",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S,%f",
)


def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    """Parse common ISO/Python logging timestamps into datetime objects.

    Naive timestamps remain naive. UTC ``Z`` suffixes are normalized to ``+00:00``.
    """
    if not value or value == "Unknown":
        return None
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(text)
        if parsed is not None:
            return parsed
    except ValueError:
        pass

    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def format_timestamp(value: Optional[datetime]) -> Optional[str]:
    """Return a stable human-readable timestamp."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")


def comparable_datetimes(left: datetime, right: datetime) -> tuple[datetime, datetime]:
    """Make two datetimes comparable by normalizing timezone awareness.

    When one timestamp has timezone information and the other does not, the
    naive value is treated as UTC. This avoids a runtime TypeError while keeping
    the behavior deterministic.
    """
    if left.tzinfo is None and right.tzinfo is not None:
        left = left.replace(tzinfo=timezone.utc)
    elif right.tzinfo is None and left.tzinfo is not None:
        right = right.replace(tzinfo=timezone.utc)
    return left, right
