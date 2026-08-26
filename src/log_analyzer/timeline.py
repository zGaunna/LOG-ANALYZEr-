def format_timeline(hourly_counts: dict, daily_counts: dict, granularity: str = 'hourly') -> str:
    """Format hourly or daily counts as a simple ASCII time series graph."""
    if granularity == 'hourly':
        data = hourly_counts
        title = "Saatlik ERROR/WARNING Dağılımı"
        # Sort keys chronologically
        sorted_keys = sorted(data.keys())
        if not sorted_keys:
            return "Veri yok"
        # Find max total count for scaling
        max_total = max((v['ERROR'] + v['WARNING']) for v in data.values()) if data else 1
        lines = [title]
        for key in sorted_keys:
            vals = data[key]
            total = vals['ERROR'] + vals['WARNING']
            # Scale to 10 chars
            error_len = int((vals['ERROR'] / max_total) * 10) if max_total > 0 else 0
            warning_len = int((vals['WARNING'] / max_total) * 10) if max_total > 0 else 0
            bar = 'E' * error_len + 'W' * warning_len
            lines.append(f"{key}: {bar} (E:{vals['ERROR']}, W:{vals['WARNING']})")
        return '\n'.join(lines)
    else:  # daily
        data = daily_counts
        title = "Günlük ERROR/WARNING Dağılımı"
        sorted_keys = sorted(data.keys())
        if not sorted_keys:
            return "Veri yok"
        max_total = max((v['ERROR'] + v['WARNING']) for v in data.values()) if data else 1
        lines = [title]
        for key in sorted_keys:
            vals = data[key]
            total = vals['ERROR'] + vals['WARNING']
            error_len = int((vals['ERROR'] / max_total) * 10) if max_total > 0 else 0
            warning_len = int((vals['WARNING'] / max_total) * 10) if max_total > 0 else 0
            bar = 'E' * error_len + 'W' * warning_len
            lines.append(f"{key}: {bar} (E:{vals['ERROR']}, W:{vals['WARNING']})")
        return '\n'.join(lines)