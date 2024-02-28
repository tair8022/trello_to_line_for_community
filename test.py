from datetime import datetime, timezone


def is_overdue(due_date_str):
    """Check if a given due date is in the past."""
    if not due_date_str:
        return False
    # 将 due_date 转换为 offset-aware datetime 对象
    due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    return due_date < now


print(is_overdue("2025-08-01T00:00:00.000Z"))