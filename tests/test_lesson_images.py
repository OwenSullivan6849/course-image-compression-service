from datetime import date, timedelta

from src.lesson_images import compression_mode


def test_deadline_within_two_days_gets_priority_processing():
    today = date(2026, 9, 4)
    assert compression_mode(today + timedelta(days=1), today) == "priority"
    assert compression_mode(today + timedelta(days=7), today) == "standard"

