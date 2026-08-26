"""Advanced analysis features for the log analyzer."""

import re
import collections
import datetime
import json
from typing import List, Tuple, Dict, Any, Optional
from .analyzer_core import LogEvent


def analyze_time_series(events: List[LogEvent]) -> Dict[str, Any]:
    """Analyze ERROR/WARNING messages over time.

    Args:
        events: List of LogEvent objects

    Returns:
        Dictionary with time series analysis results
    """
    # Group by hour
    hourly_counts = collections.defaultdict(lambda: {'ERROR': 0, 'WARNING': 0})
    daily_counts = collections.defaultdict(lambda: {'ERROR': 0, 'WARNING': 0})

    for event in events:
        if event.level not in ['ERROR', 'WARNING']:
            continue
        try:
            # Try to parse timestamp
            dt = datetime.datetime.strptime(event.timestamp, '%Y-%m-%d %H:%M:%S')
            hour_key = dt.strftime('%Y-%m-%d %H:00')
            day_key = dt.strftime('%Y-%m-%d')

            hourly_counts[hour_key][event.level] += 1
            daily_counts[day_key][event.level] += 1
        except (ValueError, TypeError):
            # Skip if timestamp format doesn't match or is None
            continue

    # Find peak hours
    peak_hour = max(hourly_counts.items(),
                   key=lambda x: x[1]['ERROR'] + x[1]['WARNING'],
                   default=(None, {'ERROR': 0, 'WARNING': 0}))

    peak_day = max(daily_counts.items(),
                  key=lambda x: x[1]['ERROR'] + x[1]['WARNING'],
                  default=(None, {'ERROR': 0, 'WARNING': 0}))

    return {
        'hourly': dict(hourly_counts),
        'daily': dict(daily_counts),
        'peak_hour': peak_hour[0] if peak_hour[0] else None,
        'peak_hour_count': peak_hour[1],
        'peak_day': peak_day[0] if peak_day[0] else None,
        'peak_day_count': peak_day[1]
    }


def analyze_error_patterns(events: List[LogEvent]) -> Dict[str, Any]:
    """Analyze patterns in error messages.

    Args:
        events: List of LogEvent objects

    Returns:
        Dictionary with error pattern analysis
    """
    # Extract just the messages for analysis
    error_messages = [event.message for event in events if event.level == 'ERROR']
    warning_messages = [event.message for event in events if event.level == 'WARNING']

    # Count word frequencies in error messages
    word_freq = collections.Counter()
    for msg in error_messages:
        # Simple word extraction (can be improved)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
        word_freq.update(words)

    # Group similar messages (basic similarity)
    message_groups = collections.defaultdict(list)
    for msg in error_messages:
        # Create a signature by removing numbers and special chars
        signature = re.sub(r'\d+', '#', msg)
        signature = re.sub(r'[^\w\s#]', '', signature).strip()
        message_groups[signature].append(msg)

    # Find most common patterns
    common_patterns = []
    for signature, msgs in message_groups.items():
        if len(msgs) > 1:
            common_patterns.append({
                'pattern': signature,
                'count': len(msgs),
                'examples': msgs[:3]  # Show first 3 examples
            })

    # Sort by count descending
    common_patterns.sort(key=lambda x: x['count'], reverse=True)

    return {
        'total_errors': len(error_messages),
        'total_warnings': len(warning_messages),
        'top_words': dict(word_freq.most_common(10)),
        'common_error_patterns': common_patterns[:10],
        'unique_error_messages': len(set(error_messages)),
        'unique_warning_messages': len(set(warning_messages))
    }


def detect_anomalies(events: List[LogEvent], threshold: float = 2.0) -> Dict[str, Any]:
    """Detect anomalous log volumes using statistical methods.

    Args:
        events: List of LogEvent objects
        threshold: Number of standard deviations for anomaly detection

    Returns:
        Dictionary with anomaly detection results
    """
    # Group by hour for time series
    hourly_total = collections.defaultdict(int)

    for event in events:
        if event.level not in ['ERROR', 'WARNING']:
            continue
        try:
            dt = datetime.datetime.strptime(event.timestamp, '%Y-%m-%d %H:%M:%S')
            hour_key = dt.strftime('%Y-%m-%d %H:00')
            hourly_total[hour_key] += 1
        except (ValueError, TypeError):
            continue

    if len(hourly_total) < 2:
        return {'anomalies': [], 'message': 'Insufficient data for anomaly detection'}

    # Calculate statistics
    counts = list(hourly_total.values())
    mean_count = sum(counts) / len(counts)
    variance = sum((x - mean_count) ** 2 for x in counts) / len(counts)
    std_count = variance ** 0.5

    # Find anomalies
    anomalies = []
    for hour_key, count in hourly_total.items():
        if std_count > 0:
            z_score = (count - mean_count) / std_count
            if abs(z_score) > threshold:
                anomalies.append({
                    'hour': hour_key,
                    'count': count,
                    'z_score': round(z_score, 2),
                    'type': 'high' if z_score > 0 else 'low'
                })

    anomalies.sort(key=lambda x: abs(x['z_score']), reverse=True)

    return {
        'mean_hourly_count': round(mean_count, 2),
        'std_hourly_count': round(std_count, 2),
        'threshold_used': threshold,
        'anomalies': anomalies,
        'total_hours_analyzed': len(hourly_total)
    }


def analyze_correlations(events: List[LogEvent]) -> Dict[str, Any]:
    """Analyze correlations between events and errors.

    Args:
        events: List of LogEvent objects

    Returns:
        Dictionary with correlation analysis
    """
    # Look for WARNINGs followed by ERRORs within 5 minutes (directed correlation)
    error_times = []
    warning_times = []

    for event in events:
        if event.level not in ['ERROR', 'WARNING']:
            continue
        try:
            dt = datetime.datetime.strptime(event.timestamp, '%Y-%m-%d %H:%M:%S')
            if event.level == 'ERROR':
                error_times.append(dt)
            elif event.level == 'WARNING':
                warning_times.append(dt)
        except (ValueError, TypeError):
            continue

    correlations = []
    # For each warning, find the first ERROR that occurs after it within 5 minutes
    for warning_time in warning_times:
        for error_time in error_times:
            time_diff = (error_time - warning_time).total_seconds()
            if 0 < time_diff <= 300:  # ERROR after WARNING, within 5 minutes
                correlations.append({
                    'warning_time': warning_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'error_time': error_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'time_diff_seconds': int(time_diff)
                })
                break  # Count each warning only once, match with first qualifying ERROR

    return {
        'warning_to_error_correlations': len(correlations),
        'correlation_examples': correlations[:5],  # Show first 5
        'total_warnings': len(warning_times),
        'total_errors': len(error_times)
    }


def generate_summary_statistics(events: List[LogEvent]) -> Dict[str, Any]:
    """Generate summary statistics from log events.

    Args:
        events: List of LogEvent objects

    Returns:
        Dictionary with summary statistics
    """
    if not events:
        return {'message': 'No messages to analyze'}

    # Basic counts
    total_events = len(events)
    error_count = sum(1 for e in events if e.level == 'ERROR')
    warning_count = sum(1 for e in events if e.level == 'WARNING')
    info_count = total_events - error_count - warning_count

    # Time range analysis
    timestamps = []
    for event in events:
        if event.timestamp and event.timestamp != 'Unknown':
            try:
                dt = datetime.datetime.strptime(event.timestamp, '%Y-%m-%d %H:%M:%S')
                timestamps.append(dt)
            except ValueError:
                continue

    time_span = None
    if timestamps:
        time_span = {
            'start': min(timestamps).strftime('%Y-%m-%d %H:%M:%S'),
            'end': max(timestamps).strftime('%Y-%m-%d %H:%M:%S'),
            'duration_hours': round((max(timestamps) - min(timestamps)).total_seconds() / 3600, 2)
        }

    # Message length statistics
    msg_lengths = [len(event.message) for event in events]
    avg_msg_length = sum(msg_lengths) / len(msg_lengths) if msg_lengths else 0

    return {
        'total_messages': total_events,
        'error_count': error_count,
        'warning_count': warning_count,
        'info_count': info_count,
        'error_percentage': round((error_count / total_events) * 100, 2) if total_events > 0 else 0,
        'warning_percentage': round((warning_count / total_events) * 100, 2) if total_events > 0 else 0,
        'time_span': time_span,
        'average_message_length': round(avg_msg_length, 2),
        'messages_per_hour': round(total_events / max(1, time_span['duration_hours']) if time_span and time_span['duration_hours'] > 0 else 0, 2)
    }