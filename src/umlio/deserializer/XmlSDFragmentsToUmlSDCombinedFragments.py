
from logging import Logger
from logging import getLogger

from untangle import Element

from umlshapes.sd.SDFragmentOperator import SDFragmentOperator
from umlshapes.sd.SDInteractionOperand import SDInteractionOperand
from umlshapes.sd.SDInteractionOperand import SDInteractionOperands
from umlshapes.sd.UmlSDCombinedFragment import UmlSDCombinedFragment

from umlio.IOTypes import Elements
from umlio.IOTypes import GraphicInformation
from umlio.IOTypes import UmlSDCombinedFragments
from umlio.IOTypes import umlSDCombinedFragmentsFactory
from umlio.XMLConstants import XmlConstants


class XmlSDFragmentsToUmlSDCombinedFragments:
    """
    Deserializes UmlSDCombinedFragment elements from untangle XML into UmlSDCombinedFragments.
    """

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def deserialize(self, umlDiagramElement: Element) -> UmlSDCombinedFragments:
        """
        Deserializes all UmlSDCombinedFragment elements from the diagram element.

        Args:
            umlDiagramElement: The untangle Element for the UMLDiagram

        Returns:
            The list of deserialized UmlSDCombinedFragment objects
        """
        umlSDCombinedFragments: UmlSDCombinedFragments = umlSDCombinedFragmentsFactory()
        fragmentElements:       Elements               = umlDiagramElement.get_elements(XmlConstants.ELEMENT_UML_SD_COMBINED_FRAGMENT)

        for fragmentElement in fragmentElements:
            self.logger.debug(f'{fragmentElement}')

            graphicInformation: GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=fragmentElement)
            rawOperator:        str                = fragmentElement[XmlConstants.ATTRIBUTE_OPERATOR]

            assert rawOperator is not None, 'I have a contract'

            operator: SDFragmentOperator = SDFragmentOperator(rawOperator)

            operandElements: Elements              = fragmentElement.get_elements(XmlConstants.ELEMENT_SD_INTERACTION_OPERAND)
            operands:        SDInteractionOperands = SDInteractionOperands([])

            for operandElement in operandElements:
                guard:         str = operandElement[XmlConstants.ATTRIBUTE_GUARD]
                startTimeStep: int = int(operandElement[XmlConstants.ATTRIBUTE_START_Y])
                endTimeStep:   int = int(operandElement[XmlConstants.ATTRIBUTE_END_Y])

                operand: SDInteractionOperand = SDInteractionOperand(
                    guard=guard,
                    startTimeStep=startTimeStep,
                    endTimeStep=endTimeStep
                )
                operands.append(operand)

            umlSDCombinedFragment: UmlSDCombinedFragment = UmlSDCombinedFragment(
                operator=operator,
                operands=operands,
                x=graphicInformation.position.x,
                y=graphicInformation.position.y,
                width=graphicInformation.size.width,
                height=graphicInformation.size.height
            )
            umlSDCombinedFragment.id       = graphicInformation.id
            umlSDCombinedFragment.size     = graphicInformation.size
            umlSDCombinedFragment.position = graphicInformation.position

            umlSDCombinedFragments.append(umlSDCombinedFragment)

        return umlSDCombinedFragments
