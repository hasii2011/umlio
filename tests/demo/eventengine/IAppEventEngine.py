
from typing import Callable
from typing import NewType

from abc import ABC
from abc import abstractmethod

from tests.demo.eventengine.DemoEventType import DemoEventType

UniqueId = NewType('UniqueId', str)


class IAppEventEngine(ABC):

    @abstractmethod
    def subscribe(self, eventType: DemoEventType, uniqueId: UniqueId, callback: Callable):
        pass

    @abstractmethod
    def sendMessage(self, eventType: DemoEventType, uniqueId: UniqueId, **kwargs):
        pass
