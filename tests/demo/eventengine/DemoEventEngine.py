
from typing import Callable

from logging import getLogger
from logging import Logger

from enum import Enum

from codeallybasic.BasePubSubEngine import BasePubSubEngine
from codeallybasic.BasePubSubEngine import Topic

from tests.demo.eventengine.DemoEventType import DemoEventType
from tests.demo.eventengine.IAppEventEngine import IAppEventEngine
from tests.demo.eventengine.IAppEventEngine import UniqueId


class DemoEventEngine(IAppEventEngine, BasePubSubEngine):

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def subscribe(self, eventType: DemoEventType, uniqueId: UniqueId, callback: Callable):
        self._subscribe(topic=self._toTopic(eventType, uniqueId), callback=callback)

    def sendMessage(self, eventType: DemoEventType, uniqueId: UniqueId, **kwargs):
        self._sendMessage(topic=self._toTopic(eventType, uniqueId), **kwargs)

    def _toTopic(self, eventType: Enum, uniqueId: str) -> Topic:
        """
        TODO: use the code ally basic version when it becomes available
        Args:
            eventType:
            uniqueId:

        Returns:

        """
        topic: Topic = Topic(f'{eventType.value}.{uniqueId}')
        return topic
