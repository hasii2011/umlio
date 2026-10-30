
from logging import Logger
from logging import getLogger
from typing import Optional

from untangle import Element

from umlmodel.SDInstance import SDInstance
from umlshapes.frames.SequenceDiagramFrame import SequenceDiagramFrame
from umlshapes.pubsubengine.IUmlPubSubEngine import IUmlPubSubEngine
from umlshapes.sd.UmlSDInstance import UmlSDInstance

from umlio.IOTypes import Elements
from umlio.IOTypes import GraphicInformation
from umlio.IOTypes import UmlSDInstances
from umlio.IOTypes import umlSDInstancesFactory
from umlio.XMLConstants import XmlConstants
from umlio.deserializer.XmlToUmlModel import XmlToUmlModel


class XmlSDInstancesToUmlSDInstances:
    """
    Deserializes UmlSDInstance elements from untangle XML into UmlSDInstances.

    Sequence diagram instance shapes (UmlSDInstance) require an active
    SequenceDiagramFrame and an IUmlPubSubEngine to host their OGL composite
    constraints and event handlers.
    """

    def __init__(self, diagramFrame: SequenceDiagramFrame, umlPubSubEngine: IUmlPubSubEngine):

        self.logger: Logger = getLogger(__name__)

        self._xmlToUmlModel:   XmlToUmlModel        = XmlToUmlModel()
        self._diagramFrame:    SequenceDiagramFrame = diagramFrame
        self._umlPubSubEngine: IUmlPubSubEngine     = umlPubSubEngine

    def deserialize(self, umlDiagramElement: Element) -> UmlSDInstances:
        """
        Deserializes all UmlSDInstance elements from the diagram element.

        Args:
            umlDiagramElement: The untangle Element for the UMLDiagram

        Returns:
            The list of deserialized UmlSDInstance objects
        """
        umlSDInstances:   UmlSDInstances = umlSDInstancesFactory()
        instanceElements: Elements       = umlDiagramElement.get_elements(XmlConstants.ELEMENT_UML_SD_INSTANCE)

        for instanceElement in instanceElements:
            self.logger.debug(f'{instanceElement}')

            graphicInformation: GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=instanceElement)
            sdInstance:         SDInstance         = self._xmlToUmlModel.sdInstanceToModelSDInstance(umlSDInstanceElement=instanceElement)

            umlSDInstance: UmlSDInstance = UmlSDInstance(
                sdInstance=sdInstance,
                diagramFrame=self._diagramFrame,
                umlPubSubEngine=self._umlPubSubEngine
            )

            umlSDInstance.id = graphicInformation.id

            if graphicInformation.size.width > 0:
                umlSDInstance.setInstanceWidth(graphicInformation.size.width)

            rawLifeLineLength: Optional[str] = instanceElement[XmlConstants.ATTRIBUTE_LIFE_LINE_LENGTH]
            if rawLifeLineLength is not None:
                lifeLineLength: int = int(rawLifeLineLength)
                umlSDInstance.setLifeLineLength(lifeLineLength)

            umlSDInstance.position = graphicInformation.position

            umlSDInstances.append(umlSDInstance)

        return umlSDInstances
