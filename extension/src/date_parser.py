"""
Date Parser

Parse simple natural-language and shorthand date/time strings into Morgen's
required due format: YYYY-MM-DDTHH:mm:ss (exactly 19 chars, no timezone).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


_WEEKDAYS = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tues": 1,
    "tuesday": 1,
    "wed": 2,
    "weds": 2,
    "wednesday": 2,
    "thu": 3,
    "thur": 3,
    "thurs": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


@dataclass(frozen=True)
class ParsedDue:
    due: str
    display: str


class DateParseError(ValueError):
    pass


class DateParser:
    """
    Parse human input for due dates.

    Supported examples:
      - today, tomorrow, next-week
      - next-mon, next-monday
      - 2026-02-10
      - 2026-02-10T15:30
      - 15:30, 3pm, 3:15pm, noon, midnight
    """

    def __init__(self, default_time: time | None = None):
        self.default_time = default_time or time(9, 0, 0)

    def parse(self, text: str, now: datetime | None = None) -> ParsedDue:
        if not text or not str(text).strip():
            raise DateParseError("Empty date")

        now = now or datetime.now()
        raw = str(text).strip().lower()
        raw = raw.replace("_", "-")
        raw = re.sub(r"\s+", " ", raw)

        dt = self._parse_datetime(raw, now=now)
        return ParsedDue(due=dt.strftime("%Y-%m-%dT%H:%M:%S"), display=dt.strftime("%Y-%m-%d %H:%M"))

    def _parse_datetime(self, raw: str, now: datetime) -> datetime:
        # Natural language
        if raw in {"today", "tod"}:
            return datetime.combine(now.date(), self.default_time)
        if raw in {"tomorrow", "tmr", "tmrw"}:
            return datetime.combine(now.date() + timedelta(days=1), self.default_time)
        if raw in {"yesterday", "yest"}:
            return datetime.combine(now.date() - timedelta(days=1), self.default_time)
        if raw in {"nextweek", "next-week"}:
            return datetime.combine(now.date() + timedelta(days=7), self.default_time)

        # next-<weekday>
        if raw.startswith("next-"):
            wd = raw[5:]
            if wd in _WEEKDAYS:
                target = _WEEKDAYS[wd]
                return datetime.combine(self._next_weekday(now.date(), target), self.default_time)
            raise DateParseError(f"Unknown weekday: {wd}")

        # Bare weekday name (e.g. "friday", "mon")
        if raw in _WEEKDAYS:
            target = _WEEKDAYS[raw]
            return datetime.combine(self._next_weekday(now.date(), target), self.default_time)

        # If it's a time-only spec, apply to today (or tomorrow if already passed)
        if self._looks_like_time(raw):
            t = self._parse_time(raw)
            candidate = datetime.combine(now.date(), t)
            if candidate < now:
                candidate = datetime.combine(now.date() + timedelta(days=1), t)
            return candidate

        # ISO-ish with optional time
        iso_match = re.fullmatch(
            r"(?P<y>\d{4})[-/](?P<m>\d{1,2})[-/](?P<d>\d{1,2})(?:[t ](?P<time>.+))?",
            raw,
        )
        if iso_match:
            y = int(iso_match.group("y"))
            m = int(iso_match.group("m"))
            d = int(iso_match.group("d"))
            base_date = self._safe_date(y, m, d)
            time_part = iso_match.group("time")
            if time_part:
                t = self._parse_time(time_part.strip())
            else:
                t = self.default_time
            return datetime.combine(base_date, t)

        # Shorthand month/day with optional time: 2/10, 02-10, 2/10T15:00
        md_match = re.fullmatch(
            r"(?P<m>\d{1,2})[-/](?P<d>\d{1,2})(?:[t ](?P<time>.+))?",
            raw,
        )
        if md_match:
            m = int(md_match.group("m"))
            d = int(md_match.group("d"))
            y = now.year
            base_date = self._safe_date(y, m, d)
            if base_date < now.date():
                base_date = self._safe_date(y + 1, m, d)
            time_part = md_match.group("time")
            t = self._parse_time(time_part.strip()) if time_part else self.default_time
            return datetime.combine(base_date, t)

        raise DateParseError(
            "Unrecognized date. Try: today, tomorrow, next-mon, 2026-02-10, 2026-02-10T15:30, 15:30"
        )

    def _looks_like_time(self, raw: str) -> bool:
        raw = raw.strip().lower()
        if raw in {"noon", "midnight"}:
            return True
        return bool(re.fullmatch(r"\d{1,2}(:\d{2})?\s*(am|pm)?", raw))

    def _parse_time(self, raw: str) -> time:
        s = raw.strip().lower()
        if s == "noon":
            return time(12, 0, 0)
        if s == "midnight":
            return time(0, 0, 0)

        m = re.fullmatch(r"(?P<h>\d{1,2})(?::(?P<min>\d{2}))?\s*(?P<ampm>am|pm)?", s)
        if not m:
            # Accept HH:MM:SS
            m2 = re.fullmatch(r"(?P<h>\d{1,2}):(?P<min>\d{2}):(?P<sec>\d{2})", s)
            if not m2:
                raise DateParseError(f"Invalid time: {raw}")
            h = int(m2.group("h"))
            minute = int(m2.group("min"))
            sec = int(m2.group("sec"))
            return self._safe_time(h, minute, sec)

        h = int(m.group("h"))
        minute = int(m.group("min") or 0)
        ampm = m.group("ampm")

        if ampm:
            if not 1 <= h <= 12:
                raise DateParseError(f"Invalid hour for {ampm}: {h}")
            if ampm == "am":
                h = 0 if h == 12 else h
            else:
                h = 12 if h == 12 else h + 12
        return self._safe_time(h, minute, 0)

    def _safe_date(self, y: int, m: int, d: int) -> date:
        try:
            return date(y, m, d)
        except ValueError as e:
            raise DateParseError(str(e))

    def _safe_time(self, h: int, minute: int, sec: int) -> time:
        try:
            return time(h, minute, sec)
        except ValueError as e:
            raise DateParseError(str(e))

    def _next_weekday(self, base: date, target_weekday: int) -> date:
        delta = (target_weekday - base.weekday()) % 7
        if delta == 0:
            delta = 7
        return base + timedelta(days=delta)

