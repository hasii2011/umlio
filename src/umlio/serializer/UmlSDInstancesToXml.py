
from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from umlshapes.sd.UmlSDInstance import UmlSDInstance

from umlio.IOTypes import ElementAttributes
from umlio.IOTypes import UmlSDInstances

from umlio.serializer.BaseUmlToXml import BaseUmlToXml
from umlio.serializer.UmlModelToXml import UmlModelToXml
from umlio.XMLConstants import XmlConstants


class UmlSDInstancesToXml(BaseUmlToXml):
    """
    Serializes UmlSDInstance shapes and their SDInstance models to XML elements.
    """
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._modelToXml: UmlModelToXml = UmlModelToXml()

    def serialize(self, documentTop: Element, umlSDInstances: UmlSDInstances) -> Element:
        """
        Serializes all UmlSDInstances in the sequence diagram.

        Args:
            documentTop:    The parent UMLDiagram XML element
            umlSDInstances: The sequence diagram instance shapes to serialize

        Returns:
            The modified documentTop element
        """
        for instance in umlSDInstances:

            umlSDInstance: UmlSDInstance = instance
            umlSDInstance.sdInstance.instanceLifeLineLength = umlSDInstance.getLifeLineLength()

            umlSDInstanceElement: Element = self._umlSDInstanceToXml(documentTop=documentTop, umlSDInstance=umlSDInstance)
            self._modelToXml.sdInstanceToXml(sdInstance=umlSDInstance.sdInstance, sdInstanceElement=umlSDInstanceElement)

        return documentTop

    def _umlSDInstanceToXml(self, documentTop: Element, umlSDInstance: UmlSDInstance) -> Element:

        attributes: ElementAttributes = self._umlBaseAttributes(umlShape=umlSDInstance)
        umlSDInstanceSubElement: Element = SubElement(
            documentTop,
            XmlConstants.ELEMENT_UML_SD_INSTANCE,
            attrib=attributes
        )

        return umlSDInstanceSubElement
