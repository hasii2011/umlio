
from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from umlshapes.sd.UmlSDMessage import UmlSDMessage

from umlio.IOTypes import ElementAttributes
from umlio.IOTypes import UmlSDMessages

from umlio.serializer.BaseUmlToXml import BaseUmlToXml
from umlio.serializer.UmlModelToXml import UmlModelToXml
from umlio.XMLConstants import XmlConstants


class UmlSDMessagesToXml(BaseUmlToXml):
    """
    Serializes UmlSDMessage shapes and their SDMessage models to XML elements.
    """
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._modelToXml: UmlModelToXml = UmlModelToXml()

    def serialize(self, documentTop: Element, umlSDMessages: UmlSDMessages) -> Element:
        """
        Serializes all UmlSDMessages in the sequence diagram.

        Args:
            documentTop:   The parent UMLDiagram XML element
            umlSDMessages: The sequence diagram message shapes to serialize

        Returns:
            The modified documentTop element
        """
        for message in umlSDMessages:

            umlSDMessage: UmlSDMessage = message
            if umlSDMessage.messageLabel is not None:
                umlSDMessage.sdMessage.message = umlSDMessage.messageLabel.label

            umlSDMessageElement: Element = self._umlSDMessageToXml(documentTop=documentTop, umlSDMessage=umlSDMessage)
            self._modelToXml.sdMessageToXml(sdMessage=umlSDMessage.sdMessage, sdMessageElement=umlSDMessageElement)

        return documentTop

    def _umlSDMessageToXml(self, documentTop: Element, umlSDMessage: UmlSDMessage) -> Element:

        attributes: ElementAttributes = ElementAttributes(
            {
                XmlConstants.ATTRIBUTE_ID:           str(umlSDMessage.id),
                XmlConstants.ATTRIBUTE_MESSAGE_TYPE: umlSDMessage.messageType.value,
            }
        )
        umlSDMessageSubElement: Element = SubElement(
            documentTop,
            XmlConstants.ELEMENT_UML_SD_MESSAGE,
            attrib=attributes
        )

        return umlSDMessageSubElement
