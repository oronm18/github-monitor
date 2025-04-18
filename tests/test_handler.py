import pytest
from datetime import datetime, timezone, timedelta
from handler import check_event
from models.event import EventType


def test_check_team_created_hacker():
    payload = {"action": "created", "team": {"name": "hackerSquad"}}
    assert check_event(EventType.TEAM, payload) is False


def test_check_team_created_not_hacker():
    payload = {"action": "created", "team": {"name": "devTeam"}}
    assert check_event(EventType.TEAM, payload) is True


def test_check_repo_deleted_after_10_minutes():
    now = datetime.now(timezone.utc)
    created_at = (now - timedelta(seconds=700)).isoformat()
    payload = {
        "action": "deleted",
        "repository": {"created_at": created_at}
    }
    assert check_event(EventType.REPOSITORY, payload) is True

def test_check_repo_deleted_before_10_minutes():
    now = datetime.now(timezone.utc)
    created_at = (now - timedelta(seconds=200)).isoformat()
    payload = {
        "action": "deleted",
        "repository": {"created_at": created_at}
    }
    assert check_event(EventType.REPOSITORY, payload) is False


def test_check_push_suspicious_hour():
    ts = datetime(2025, 1, 1, 15, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
    payload = {"head_commit": {"timestamp": ts}}
    assert check_event(EventType.PUSH, payload) is False


def test_check_push_border_hours():
    ts = datetime(2025, 1, 1, 13, 30, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
    payload = {"head_commit": {"timestamp": ts}}
    assert check_event(EventType.PUSH, payload) is True
