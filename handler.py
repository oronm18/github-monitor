"""Implement the handler and the sus behave logic."""
import logging
from datetime import datetime, timezone

from models.event import EventType


def check_event(x_github_event: str, payload: dict) -> bool:
    match x_github_event:
        case EventType.TEAM:
            return check_team(payload)

        case EventType.REPOSITORY:
            return check_repo(payload)

        case EventType.PUSH:
            return check_push(payload)

        case _:
            logging.info(f'We dont handle {x_github_event} event yet.')
            return True


def check_team(payload: dict) -> bool:
    team_name: str = payload.get('team', {}).get('name', '')
    if payload.get('action') == 'created' and team_name.startswith('hacker'):
        return False
    return True


def check_repo(payload: dict) -> bool:
    created_at = datetime.fromisoformat(payload.get('repository', {}).get('created_at').replace('Z', '+00:00'))
    time_since_created = datetime.now(timezone.utc) - created_at
    if payload.get('action') == 'deleted' and time_since_created.total_seconds() < 600:
        return False
    return True


def check_push(payload: dict) -> bool:
    ts = payload.get('head_commit', {}).get('timestamp')
    if 14  < datetime.fromisoformat(ts.rstrip('Z')).hour < 16:
        return False
    return True