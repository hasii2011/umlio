
from typing import Callable
from typing import NewType

from abc import ABC
from abc import abstractmethod

from tests.demo.pubsubengine.DemoMessageType import DemoMessageType

UniqueId = NewType('UniqueId', str)


class IAppPubSubEngine(ABC):

    @abstractmethod
    def subscribe(self, eventType: DemoMessageType, uniqueId: UniqueId, callback: Callable):
        pass

    @abstractmethod
    def sendMessage(self, eventType: DemoMessageType, uniqueId: UniqueId, **kwargs):
        pass
