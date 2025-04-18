import logging

from notifiers.base import Notifier

class LogNotify(Notifier):
    def notify(self, event_type: str, payload: dict) -> None:
        logging.info(f'Received {event_type} event with {payload=}.\n')