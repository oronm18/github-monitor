from enum import StrEnum

class EventType(StrEnum):
    PUSH = 'push'
    TEAM = 'team'
    REPOSITORY = 'repository'
    DELETE = 'delete'
