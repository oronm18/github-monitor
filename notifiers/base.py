"""Implement the base notifier"""
import abc


class Notifier(abc.ABC):
    @abc.abstractmethod
    def notify(self, event_type: str, payload: dict) -> None:
        pass