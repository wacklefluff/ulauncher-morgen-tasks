import sys
from datetime import datetime, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from date_parser import DateParser, DateParseError


def test_today_uses_default_time():
    now = datetime(2026, 2, 6, 8, 30, 0)
    parsed = DateParser(default_time=time(9, 0, 0)).parse("today", now=now)
    assert parsed.due == "2026-02-06T09:00:00"
    assert parsed.display == "2026-02-06 09:00"


def test_tomorrow_uses_default_time():
    now = datetime(2026, 2, 6, 8, 30, 0)
    parsed = DateParser(default_time=time(9, 0, 0)).parse("tomorrow", now=now)
    assert parsed.due == "2026-02-07T09:00:00"


def test_yesterday_uses_default_time():
    now = datetime(2026, 2, 6, 8, 30, 0)
    parsed = DateParser(default_time=time(9, 0, 0)).parse("yesterday", now=now)
    assert parsed.due == "2026-02-05T09:00:00"


def test_bare_weekday_is_next_occurrence_not_same_day():
    # 2026-02-06 is a Friday; "friday" should mean next Friday.
    now = datetime(2026, 2, 6, 12, 0, 0)
    parsed = DateParser(default_time=time(9, 0, 0)).parse("friday", now=now)
    assert parsed.due == "2026-02-13T09:00:00"


def test_next_weekday_works():
    now = datetime(2026, 2, 6, 12, 0, 0)
    parsed = DateParser(default_time=time(9, 0, 0)).parse("next-fri", now=now)
    assert parsed.due == "2026-02-13T09:00:00"


def test_time_only_rolls_to_tomorrow_if_time_has_passed():
    now = datetime(2026, 2, 6, 10, 0, 0)
    parsed = DateParser().parse("09:00", now=now)
    assert parsed.due == "2026-02-07T09:00:00"


def test_iso_date_with_time():
    now = datetime(2026, 2, 6, 12, 0, 0)
    parsed = DateParser().parse("2026-02-10T15:30", now=now)
    assert parsed.due == "2026-02-10T15:30:00"


def test_invalid_date_raises():
    now = datetime(2026, 2, 6, 12, 0, 0)
    with pytest.raises(DateParseError):
        DateParser().parse("notadate", now=now)

