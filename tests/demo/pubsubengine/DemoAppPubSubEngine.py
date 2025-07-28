
from typing import Callable

from logging import getLogger
from logging import Logger

from enum import Enum

from codeallybasic.BasePubSubEngine import BasePubSubEngine
from codeallybasic.BasePubSubEngine import Topic

from tests.demo.pubsubengine.DemoMessageType import DemoMessageType
from tests.demo.pubsubengine.IAppPubSubEngine import IAppPubSubEngine
from tests.demo.pubsubengine.IAppPubSubEngine import UniqueId


class DemoAppPubSubEngine(IAppPubSubEngine, BasePubSubEngine):

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def subscribe(self, eventType: DemoMessageType, uniqueId: UniqueId, callback: Callable):
        self._subscribe(topic=self._toTopic(eventType, uniqueId), callback=callback)

    def sendMessage(self, eventType: DemoMessageType, uniqueId: UniqueId, **kwargs):
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
