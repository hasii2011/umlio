
from typing import cast

from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from umlshapes.sd.UmlSDExecution import UmlSDExecution

from umlio.IOTypes import ElementAttributes
from umlio.IOTypes import UmlSDExecutions

from umlio.serializer.BaseUmlToXml import BaseUmlToXml
from umlio.serializer.UmlModelToXml import UmlModelToXml
from umlio.XMLConstants import XmlConstants


class UmlSDExecutionsToXml(BaseUmlToXml):
    """
    Serializes UmlSDExecution shapes (activation bars) and their SDExecution models to XML elements.
    """
    def __init__(self):
        super().__init__()
        self.logger:      Logger        = getLogger(__name__)
        self._modelToXml: UmlModelToXml = UmlModelToXml()

    def serialize(self, documentTop: Element, umlSDExecutions: UmlSDExecutions) -> Element:
        """
        Serializes all UmlSDExecutions in the sequence diagram.

        Args:
            documentTop:     The parent UMLDiagram XML element
            umlSDExecutions: The sequence diagram execution shapes to serialize

        Returns:
            The modified documentTop element
        """
        for execution in umlSDExecutions:
            umlSDExecution:        UmlSDExecution = cast(UmlSDExecution, execution)
            umlSDExecutionElement: Element        = self._umlSDExecutionToXml(documentTop=documentTop, umlSDExecution=umlSDExecution)
            if umlSDExecution.sdExecution is not None:
                self._modelToXml.sdExecutionToXml(sdExecution=umlSDExecution.sdExecution, sdExecutionElement=umlSDExecutionElement)

        return documentTop

    def _umlSDExecutionToXml(self, documentTop: Element, umlSDExecution: UmlSDExecution) -> Element:

        attributes: ElementAttributes = ElementAttributes(
            {
                XmlConstants.ATTRIBUTE_ID: str(umlSDExecution.id),
            }
        )
        umlSDExecutionSubElement: Element = SubElement(
            documentTop,
            XmlConstants.ELEMENT_UML_SD_EXECUTION,
            attrib=attributes
        )

        return umlSDExecutionSubElement
