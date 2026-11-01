
from unittest import defaultTestLoader
from unittest import TestSuite
from unittest import main as unitTestMain

from pathlib import Path

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW
from codeallybasic.UnitTestBase import UnitTestBase

from umlshapes.lib.ogl import OGLInitialize
from umlshapes.sd.SDFragmentOperator import SDFragmentOperator
from umlshapes.sd.SDMessageType import SDMessageType
from umlshapes.sd.UmlSDCombinedFragment import UmlSDCombinedFragment
from umlshapes.sd.UmlSDExecution import UmlSDExecution
from umlshapes.sd.UmlSDInstance import UmlSDInstance
from umlshapes.sd.UmlSDMessage import UmlSDMessage

from umlio.IOTypes import UmlDocument
from umlio.IOTypes import UmlDocumentTitle
from umlio.IOTypes import UmlDocumentType
from umlio.IOTypes import UmlProject
from umlio.Reader import Reader
from umlio.deserializer.XmlToUmlShapes import XmlToUmlShapes

from tests.umlio.GoldenFileConstants import SEQUENCE_DIAGRAM_XML_PROJECT

from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_INSTANCE_ID
from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_INSTANCE_NAME
from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_INSTANCE_X
from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_MODEL_ID
from tests.umlio.SequenceDiagramTestConstants import DEFAULT_LIFELINE_LENGTH
from tests.umlio.SequenceDiagramTestConstants import EMPTY_SD_DIAGRAM_XML
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_END_Y
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_MODEL_ID
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_NESTING_LEVEL
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_OPERATION_NAME
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_ORDER_SERVICE_ID
from tests.umlio.SequenceDiagramTestConstants import EXECUTION_START_Y
from tests.umlio.SequenceDiagramTestConstants import EXPECTED_SEQUENCE_DIAGRAM_XML
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_ALT_ID
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_HEIGHT
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_WIDTH
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_X
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_Y
from tests.umlio.SequenceDiagramTestConstants import INSTANCE_Y
from tests.umlio.SequenceDiagramTestConstants import MESSAGE_MODEL_ID
from tests.umlio.SequenceDiagramTestConstants import MESSAGE_PLACE_ORDER_ID
from tests.umlio.SequenceDiagramTestConstants import MESSAGE_TEXT
from tests.umlio.SequenceDiagramTestConstants import MESSAGE_TIME_STEP
from tests.umlio.SequenceDiagramTestConstants import OPERAND_1_END_Y
from tests.umlio.SequenceDiagramTestConstants import OPERAND_1_GUARD
from tests.umlio.SequenceDiagramTestConstants import OPERAND_1_START_Y
from tests.umlio.SequenceDiagramTestConstants import OPERAND_2_END_Y
from tests.umlio.SequenceDiagramTestConstants import OPERAND_2_GUARD
from tests.umlio.SequenceDiagramTestConstants import OPERAND_2_START_Y
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_INSTANCE_ID
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_INSTANCE_NAME
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_INSTANCE_X
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_MODEL_ID
from tests.umlio.UmlIOBaseTest import UmlIOBaseTest

ORDER_PROCESSING_TITLE: str = 'Order Processing'


class TestSequenceDiagramDeserialization(UnitTestBaseW):
    """
    Integration tests for sequence diagram deserialization through XmlToUmlShapes and Reader.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        OGLInitialize()

    def tearDown(self):
        super().tearDown()

    def testDeserializeXmlFromString(self):
        diagramXml: str = EXPECTED_SEQUENCE_DIAGRAM_XML.split('\n', 1)[1]
        xmlProjectString: str = (
            "<?xml version='1.0' encoding='iso-8859-1'?>\n"
            '<UmlProject fileName="/Users/humberto.a.sanchez.ii/SampleProject.udt" version="14.0" codePath="/Users/humberto.a.sanchez.ii">\n'
            f'{diagramXml}\n'
            '</UmlProject>'
        )

        xmlToUmlShapes: XmlToUmlShapes = XmlToUmlShapes()
        xmlToUmlShapes.deserializeXml(xmlString=xmlProjectString, fileName=Path('sample.xml'))

        umlProject: UmlProject = xmlToUmlShapes.umlProject
        self.assertIn(UmlDocumentTitle(ORDER_PROCESSING_TITLE), umlProject.umlDocuments)

        umlDocument: UmlDocument = umlProject.umlDocuments[UmlDocumentTitle(ORDER_PROCESSING_TITLE)]
        self._verifyDeserializedDocument(umlDocument=umlDocument)

    def testDeserializeGoldenFile(self):
        goldenFilePath: str = UnitTestBase.getFullyQualifiedResourceFileName(
            package=UmlIOBaseTest.GOLDEN_FILES_PACKAGE_NAME,
            fileName=SEQUENCE_DIAGRAM_XML_PROJECT
        )

        reader:     Reader     = Reader()
        umlProject: UmlProject = reader.readXmlFile(fileName=Path(goldenFilePath))

        self.assertIn(UmlDocumentTitle(ORDER_PROCESSING_TITLE), umlProject.umlDocuments)

        umlDocument: UmlDocument = umlProject.umlDocuments[UmlDocumentTitle(ORDER_PROCESSING_TITLE)]
        self._verifyDeserializedDocument(umlDocument=umlDocument)

    def testDeserializeEmptySequenceDiagram(self):
        diagramXml: str = EMPTY_SD_DIAGRAM_XML.split('\n', 1)[1]
        xmlProjectString: str = (
            "<?xml version='1.0' encoding='iso-8859-1'?>\n"
            '<UmlProject fileName="/Users/humberto.a.sanchez.ii/SampleProject.udt" version="14.0" codePath="/Users/humberto.a.sanchez.ii">\n'
            f'{diagramXml}\n'
            '</UmlProject>'
        )

        xmlToUmlShapes: XmlToUmlShapes = XmlToUmlShapes()
        xmlToUmlShapes.deserializeXml(xmlString=xmlProjectString, fileName=Path('empty.xml'))

        umlProject: UmlProject = xmlToUmlShapes.umlProject
        self.assertIn(UmlDocumentTitle('Empty SD Diagram'), umlProject.umlDocuments)

        umlDocument: UmlDocument = umlProject.umlDocuments[UmlDocumentTitle('Empty SD Diagram')]
        self.assertEqual(UmlDocumentType.SEQUENCE_DOCUMENT, umlDocument.documentType)
        self.assertEqual(0, len(umlDocument.umlSDInstances))
        self.assertEqual(0, len(umlDocument.umlSDMessages))
        self.assertEqual(0, len(umlDocument.umlSDExecutions))
        self.assertEqual(0, len(umlDocument.umlSDCombinedFragments))

    def _verifyDeserializedDocument(self, umlDocument: UmlDocument):
        self.assertEqual(UmlDocumentType.SEQUENCE_DOCUMENT, umlDocument.documentType)

        # Instances
        self.assertEqual(2, len(umlDocument.umlSDInstances), 'Expected 2 instances')
        customerInstance:     UmlSDInstance = umlDocument.umlSDInstances[0]
        orderServiceInstance: UmlSDInstance = umlDocument.umlSDInstances[1]

        self.assertEqual(CUSTOMER_INSTANCE_ID, customerInstance.id)
        self.assertEqual(CUSTOMER_MODEL_ID, customerInstance.sdInstance.id)
        self.assertEqual(CUSTOMER_INSTANCE_NAME, customerInstance.sdInstance.instanceName)
        self.assertEqual(CUSTOMER_INSTANCE_X, customerInstance.position.x)
        self.assertEqual(INSTANCE_Y, customerInstance.position.y)
        self.assertEqual(DEFAULT_LIFELINE_LENGTH, customerInstance.getLifeLineLength())

        self.assertEqual(ORDER_SERVICE_INSTANCE_ID, orderServiceInstance.id)
        self.assertEqual(ORDER_SERVICE_MODEL_ID, orderServiceInstance.sdInstance.id)
        self.assertEqual(ORDER_SERVICE_INSTANCE_NAME, orderServiceInstance.sdInstance.instanceName)
        self.assertEqual(ORDER_SERVICE_INSTANCE_X, orderServiceInstance.position.x)
        self.assertEqual(INSTANCE_Y, orderServiceInstance.position.y)
        self.assertEqual(DEFAULT_LIFELINE_LENGTH, orderServiceInstance.getLifeLineLength())

        # Messages
        self.assertEqual(1, len(umlDocument.umlSDMessages), 'Expected 1 message')
        message: UmlSDMessage = umlDocument.umlSDMessages[0]
        self.assertEqual(MESSAGE_PLACE_ORDER_ID, message.id)
        self.assertEqual(MESSAGE_MODEL_ID, message.sdMessage.id)
        self.assertEqual(MESSAGE_TEXT, message.sdMessage.message)
        self.assertEqual(SDMessageType.SYNCHRONOUS, message.messageType)
        self.assertEqual(MESSAGE_TIME_STEP, message.fromY)
        self.assertEqual(MESSAGE_TIME_STEP, message.toY)
        self.assertIsNotNone(message.sdMessage.source)
        self.assertEqual(CUSTOMER_MODEL_ID, message.sdMessage.source.id)
        self.assertIsNotNone(message.sdMessage.destination)
        self.assertEqual(ORDER_SERVICE_MODEL_ID, message.sdMessage.destination.id)

        # Executions
        self.assertEqual(1, len(umlDocument.umlSDExecutions), 'Expected 1 execution')
        execution: UmlSDExecution = umlDocument.umlSDExecutions[0]
        self.assertEqual(EXECUTION_ORDER_SERVICE_ID, execution.id)
        self.assertEqual(EXECUTION_START_Y, execution.startY)
        self.assertEqual(EXECUTION_END_Y, execution.endY)
        self.assertEqual(EXECUTION_NESTING_LEVEL, execution.nestingLevel)
        self.assertEqual(EXECUTION_OPERATION_NAME, execution.operation)
        self.assertIsNotNone(execution.sdExecution)
        self.assertEqual(EXECUTION_MODEL_ID, execution.sdExecution.id)
        self.assertIsNotNone(execution.sdExecution.instance)
        self.assertEqual(ORDER_SERVICE_MODEL_ID, execution.sdExecution.instance.id)

        # Combined Fragments
        self.assertEqual(1, len(umlDocument.umlSDCombinedFragments), 'Expected 1 combined fragment')
        fragment: UmlSDCombinedFragment = umlDocument.umlSDCombinedFragments[0]
        self.assertEqual(FRAGMENT_ALT_ID, fragment.id)
        self.assertEqual(SDFragmentOperator.ALT, fragment.operator)
        self.assertEqual(FRAGMENT_X, fragment.position.x)
        self.assertEqual(FRAGMENT_Y, fragment.position.y)
        self.assertEqual(FRAGMENT_WIDTH, fragment.size.width)
        self.assertEqual(FRAGMENT_HEIGHT, fragment.size.height)
        self.assertEqual(2, len(fragment.operands))
        self.assertEqual(OPERAND_1_GUARD, fragment.operands[0].guard)
        self.assertEqual(OPERAND_1_START_Y, fragment.operands[0].startTimeStep)
        self.assertEqual(OPERAND_1_END_Y, fragment.operands[0].endTimeStep)
        self.assertEqual(OPERAND_2_GUARD, fragment.operands[1].guard)
        self.assertEqual(OPERAND_2_START_Y, fragment.operands[1].startTimeStep)
        self.assertEqual(OPERAND_2_END_Y, fragment.operands[1].endTimeStep)


def suite() -> TestSuite:
    testSuite: TestSuite = defaultTestLoader.loadTestsFromTestCase(TestSequenceDiagramDeserialization)
    return testSuite


if __name__ == '__main__':
    unitTestMain()
