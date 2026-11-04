
from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from umlshapes.sd.SDInteractionOperand import SDInteractionOperand
from umlshapes.sd.UmlSDCombinedFragment import UmlSDCombinedFragment

from umlio.IOTypes import ElementAttributes
from umlio.IOTypes import UmlSDCombinedFragments

from umlio.serializer.BaseUmlToXml import BaseUmlToXml
from umlio.XMLConstants import XmlConstants


class UmlSDCombinedFragmentsToXml(BaseUmlToXml):
    """
    Serializes UmlSDCombinedFragment shapes and their operands to XML elements.
    """
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def serialize(self, documentTop: Element, umlSDCombinedFragments: UmlSDCombinedFragments) -> Element:
        """
        Serializes all UmlSDCombinedFragments in the sequence diagram.

        Args:
            documentTop:            The parent UMLDiagram XML element
            umlSDCombinedFragments: The sequence diagram combined fragment shapes to serialize

        Returns:
            The modified documentTop element
        """
        for fragment in umlSDCombinedFragments:

            umlSDCombinedFragment: UmlSDCombinedFragment = fragment
            self._umlSDCombinedFragmentToXml(documentTop=documentTop, umlSDCombinedFragment=umlSDCombinedFragment)

        return documentTop

    def _umlSDCombinedFragmentToXml(self, documentTop: Element, umlSDCombinedFragment: UmlSDCombinedFragment) -> Element:

        width:  int = round(umlSDCombinedFragment.GetWidth())
        height: int = round(umlSDCombinedFragment.GetHeight())
        leftX:  int = round(umlSDCombinedFragment.GetX() - (width / 2.0))
        topY:   int = round(umlSDCombinedFragment.GetY() - (height / 2.0))

        attributes: ElementAttributes = ElementAttributes(
            {
                XmlConstants.ATTRIBUTE_ID:       str(umlSDCombinedFragment.id),
                XmlConstants.ATTRIBUTE_WIDTH:    str(width),
                XmlConstants.ATTRIBUTE_HEIGHT:   str(height),
                XmlConstants.ATTRIBUTE_X:        str(leftX),
                XmlConstants.ATTRIBUTE_Y:        str(topY),
                XmlConstants.ATTRIBUTE_OPERATOR: umlSDCombinedFragment.operator.value,
            }
        )

        fragmentSubElement: Element = SubElement(
            documentTop,
            XmlConstants.ELEMENT_UML_SD_COMBINED_FRAGMENT,
            attrib=attributes
        )

        for operand in umlSDCombinedFragment.operands:
            sdOperand: SDInteractionOperand = operand
            operandAttributes: ElementAttributes = ElementAttributes(
                {
                    XmlConstants.ATTRIBUTE_GUARD:   sdOperand.guard,
                    XmlConstants.ATTRIBUTE_START_Y: str(sdOperand.startTimeStep),
                    XmlConstants.ATTRIBUTE_END_Y:   str(sdOperand.endTimeStep),
                }
            )
            SubElement(
                fragmentSubElement,
                XmlConstants.ELEMENT_SD_INTERACTION_OPERAND,
                attrib=operandAttributes
            )

        return fragmentSubElement
