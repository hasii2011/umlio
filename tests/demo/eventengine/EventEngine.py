
from typing import Callable

from logging import Logger
from logging import getLogger

from codeallybasic.SingletonV3 import SingletonV3

from tests.demo.eventengine.BaseEventEngine import Topic
from tests.demo.eventengine.EventType import EventType
from tests.demo.eventengine.BaseEventEngine import BaseEventEngine


class EventEngine(BaseEventEngine, metaclass=SingletonV3):

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def registerListener(self, event: EventType, callback: Callable):
        self._subscribe(topic=Topic(event.value), callback=callback)

    def sendEvent(self, eventType: EventType, **kwargs):
        self._sendMessage(topic=Topic(eventType.value), **kwargs)
