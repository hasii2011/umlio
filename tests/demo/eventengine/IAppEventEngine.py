
from typing import Callable
from typing import NewType

from abc import ABC
from abc import abstractmethod

from tests.demo.eventengine.DemoEventType import DemoEventType

UniqueId = NewType('UniqueId', str)


class IAppEventEngine(ABC):

    @abstractmethod
    def registerListener(self, eventType: DemoEventType, uniqueId: UniqueId, callback: Callable):
        pass

    @abstractmethod
    def sendEvent(self, eventType: DemoEventType, uniqueId: UniqueId, **kwargs):
        pass
