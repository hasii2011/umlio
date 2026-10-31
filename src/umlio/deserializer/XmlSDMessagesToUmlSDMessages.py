
from logging import Logger
from logging import getLogger
from typing import Optional

from untangle import Element

from umlmodel.SDInstance import SDInstance
from umlmodel.SDMessage import SDMessage
from umlshapes.sd.SDMessageType import SDMessageType
from umlshapes.sd.UmlSDInstance import UmlSDInstance
from umlshapes.sd.UmlSDMessage import UmlSDMessage

from umlio.IOTypes import Elements
from umlio.IOTypes import UmlSDInstances
from umlio.IOTypes import UmlSDMessages
from umlio.IOTypes import umlSDMessagesFactory
from umlio.XMLConstants import XmlConstants
from umlio.deserializer.XmlToUmlModel import SDMessageDeserializationInfo
from umlio.deserializer.XmlToUmlModel import XmlToUmlModel


class XmlSDMessagesToUmlSDMessages:
    """
    Deserializes UmlSDMessage elements from untangle XML into UmlSDMessages.
    """

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._xmlToUmlModel: XmlToUmlModel = XmlToUmlModel()

    def deserialize(self, umlDiagramElement: Element, umlSDInstances: UmlSDInstances) -> UmlSDMessages:
        """
        Deserializes all UmlSDMessage elements from the diagram element.

        Args:
            umlDiagramElement: The untangle Element for the UMLDiagram
            umlSDInstances:    The already deserialized sequence diagram instances for endpoint resolution

        Returns:
            The list of deserialized UmlSDMessage objects
        """
        umlSDMessages:   UmlSDMessages = umlSDMessagesFactory()
        messageElements: Elements      = umlDiagramElement.get_elements(XmlConstants.ELEMENT_UML_SD_MESSAGE)

        instanceMap: dict[str, UmlSDInstance] = {}
        for instance in umlSDInstances:
            instanceMap[instance.id] = instance
            instanceMap[instance.sdInstance.id] = instance

        for messageElement in messageElements:
            self.logger.debug(f'{messageElement}')

            messageId:      str           = messageElement[XmlConstants.ATTRIBUTE_ID]
            rawMessageType: Optional[str] = messageElement[XmlConstants.ATTRIBUTE_MESSAGE_TYPE]
            messageType:    SDMessageType

            if rawMessageType is not None:
                messageType = SDMessageType(rawMessageType)
            else:
                messageType = SDMessageType.SYNCHRONOUS

            sdMessageInfo: SDMessageDeserializationInfo = self._xmlToUmlModel.sdMessageToModelSDMessage(umlSDMessageElement=messageElement)
            sdMessage:     SDMessage                    = sdMessageInfo.sdMessage
            sourceId:      str                          = sdMessageInfo.sourceId
            destinationId: str                          = sdMessageInfo.destinationId

            sourceInstance: Optional[UmlSDInstance] = instanceMap.get(sourceId)
            destInstance:   Optional[UmlSDInstance] = instanceMap.get(destinationId)

            if sourceInstance is not None:
                sdMessage.source = sourceInstance.sdInstance
            if destInstance is not None:
                sdMessage.destination = destInstance.sdInstance

            umlSDMessage: UmlSDMessage = UmlSDMessage(
                sdMessage=sdMessage,
                messageType=messageType
            )
            umlSDMessage.id = messageId

            if sourceInstance is not None:
                umlSDMessage.SetFrom(sourceInstance.umlSDLifeLine)
            if destInstance is not None:
                umlSDMessage.SetTo(destInstance.umlSDLifeLine)

            umlSDMessage.fromY = sdMessage.sourceY
            umlSDMessage.toY   = sdMessage.destinationY
            umlSDMessage.updateMessage()

            umlSDMessages.append(umlSDMessage)

        return umlSDMessages
