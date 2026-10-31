
from unittest import defaultTestLoader
from unittest import TestSuite
from unittest import main as unitTestMain

from untangle import Element
from untangle import parse

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from umlshapes.lib.ogl import OGLInitialize
from umlshapes.sd.UmlSDExecution import UmlSDExecution

from umlio.IOTypes import UmlSDExecutions
from umlio.IOTypes import UmlSDInstances
from umlio.deserializer.XmlSDInstancesToUmlSDInstances import XmlSDInstancesToUmlSDInstances
from umlio.deserializer.XmlSDExecutionsToUmlSDExecutions import XmlSDExecutionsToUmlSDExecutions

from tests.umlio.SequenceDiagramTestConstants import EMPTY_SD_DIAGRAM_XML
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_END_Y
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_MODEL_ID
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_NESTING_LEVEL
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_OPERATION_NAME
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_ORDER_SERVICE_ID
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_START_Y
from tests.umlio.SequenceDiagramTestConstants import EXPECTED_SD_EXECUTIONS_XML
from tests.umlio.SequenceDiagramTestConstants import EXPECTED_SD_INSTANCES_XML
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_MODEL_ID


class TestXmlSDExecutionsToUmlSDExecutions(UnitTestBaseW):
    """
    Unit tests verifying deserialization of UmlSDExecution elements.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        OGLInitialize()

    def testEmptyDiagramDeserialization(self):
        root:              Element                          = parse(EMPTY_SD_DIAGRAM_XML)
        diagramElement:    Element                          = root.UMLDiagram
        emptyInstances:    UmlSDInstances                   = UmlSDInstances([])
        deserializer:      XmlSDExecutionsToUmlSDExecutions = XmlSDExecutionsToUmlSDExecutions()
        deserializedExecs: UmlSDExecutions                  = deserializer.deserialize(
            umlDiagramElement=diagramElement,
            umlSDInstances=emptyInstances
        )

        self.assertEqual(0, len(deserializedExecs), 'Expected 0 executions for empty diagram')

    def testExecutionDeserialization(self):
        instancesRoot:         Element                        = parse(EXPECTED_SD_INSTANCES_XML)
        instancesDiagramElem:  Element                        = instancesRoot.UMLDiagram
        instancesDeserializer: XmlSDInstancesToUmlSDInstances = XmlSDInstancesToUmlSDInstances()
        deserializedInstances: UmlSDInstances                 = instancesDeserializer.deserialize(umlDiagramElement=instancesDiagramElem)

        executionsRoot:        Element                          = parse(EXPECTED_SD_EXECUTIONS_XML)
        executionsDiagramElem: Element                          = executionsRoot.UMLDiagram
        deserializer:          XmlSDExecutionsToUmlSDExecutions = XmlSDExecutionsToUmlSDExecutions()
        deserializedExecs:     UmlSDExecutions                  = deserializer.deserialize(
            umlDiagramElement=executionsDiagramElem,
            umlSDInstances=deserializedInstances
        )

        self.assertEqual(1, len(deserializedExecs), 'Expected 1 execution deserialized')

        execution: UmlSDExecution = deserializedExecs[0]
        self.assertEqual(EXECUTION_ORDER_SERVICE_ID, execution.id)
        self.assertEqual(EXECUTION_START_Y, execution.startY)
        self.assertEqual(EXECUTION_END_Y, execution.endY)
        self.assertEqual(EXECUTION_NESTING_LEVEL, execution.nestingLevel)
        self.assertEqual(EXECUTION_OPERATION_NAME, execution.operation)

        self.assertIsNotNone(execution.sdExecution)
        self.assertEqual(EXECUTION_MODEL_ID, execution.sdExecution.id)
        self.assertIsNotNone(execution.sdExecution.instance)
        self.assertEqual(ORDER_SERVICE_MODEL_ID, execution.sdExecution.instance.id)

        targetInstance = deserializedInstances[1]
        self.assertEqual(targetInstance.umlSDLifeLine, execution.lifeLine)


def suite() -> TestSuite:
    testSuite: TestSuite = defaultTestLoader.loadTestsFromTestCase(TestXmlSDExecutionsToUmlSDExecutions)
    return testSuite


if __name__ == '__main__':
    unitTestMain()
