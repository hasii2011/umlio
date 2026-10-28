
from logging import Logger
from logging import getLogger
from typing import Optional

from untangle import Element

from umlmodel.SDExecution import SDExecution
from umlshapes.sd.UmlSDExecution import UmlSDExecution
from umlshapes.sd.UmlSDInstance import UmlSDInstance

from umlio.IOTypes import Elements
from umlio.IOTypes import UmlSDExecutions
from umlio.IOTypes import UmlSDInstances
from umlio.IOTypes import umlSDExecutionsFactory
from umlio.XMLConstants import XmlConstants
from umlio.deserializer.XmlToUmlModel import SDExecutionDeserializationInfo
from umlio.deserializer.XmlToUmlModel import XmlToUmlModel


class XmlSDExecutionsToUmlSDExecutions:
    """
    Deserializes UmlSDExecution elements from untangle XML into UmlSDExecutions.
    """

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._xmlToUmlModel: XmlToUmlModel = XmlToUmlModel()

    def deserialize(self, umlDiagramElement: Element, umlSDInstances: UmlSDInstances) -> UmlSDExecutions:
        """
        Deserializes all UmlSDExecution elements from the diagram element.

        Args:
            umlDiagramElement: The untangle Element for the UMLDiagram
            umlSDInstances:    The already deserialized sequence diagram instances for lifeline resolution

        Returns:
            The list of deserialized UmlSDExecution objects
        """
        umlSDExecutions:   UmlSDExecutions = umlSDExecutionsFactory()
        executionElements: Elements        = umlDiagramElement.get_elements(XmlConstants.ELEMENT_UML_SD_EXECUTION)

        instanceMap: dict[str, UmlSDInstance] = {}
        for instance in umlSDInstances:
            instanceMap[instance.id]            = instance
            instanceMap[instance.sdInstance.id] = instance

        for executionElement in executionElements:
            self.logger.debug(f'{executionElement}')

            executionId: str = executionElement[XmlConstants.ATTRIBUTE_ID]

            sdExecutionInfo: SDExecutionDeserializationInfo = self._xmlToUmlModel.sdExecutionToModelSDExecution(
                umlSDExecutionElement=executionElement
            )
            sdExecution: SDExecution = sdExecutionInfo.sdExecution
            instanceId:  str         = sdExecutionInfo.instanceId

            targetInstance: Optional[UmlSDInstance] = instanceMap.get(instanceId)
            assert targetInstance is not None, f'Instance with id {instanceId} not found for execution {executionId}'

            sdExecution.instance = targetInstance.sdInstance

            umlSDExecution: UmlSDExecution = UmlSDExecution(
                lifeLine=targetInstance.umlSDLifeLine,
                startY=sdExecution.startTime,
                endY=sdExecution.endTime,
                nestingLevel=sdExecution.nestingLevel,
                sdExecution=sdExecution
            )
            umlSDExecution.id = executionId

            umlSDExecutions.append(umlSDExecution)

        return umlSDExecutions
