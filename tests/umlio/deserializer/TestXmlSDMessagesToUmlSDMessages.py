
from unittest import defaultTestLoader
from unittest import TestSuite
from unittest import main as unitTestMain

from untangle import Element
from untangle import parse

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from umlshapes.lib.ogl import OGLInitialize
from umlshapes.sd.SDMessageType import SDMessageType
from umlshapes.sd.UmlSDMessage import UmlSDMessage

from umlio.IOTypes import UmlSDInstances
from umlio.IOTypes import UmlSDMessages
from umlio.deserializer.XmlSDInstancesToUmlSDInstances import XmlSDInstancesToUmlSDInstances
from umlio.deserializer.XmlSDMessagesToUmlSDMessages import XmlSDMessagesToUmlSDMessages

from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_MODEL_ID
from tests.umlio.SequenceDiagramTestConstants import EMPTY_SD_DIAGRAM_XML
from tests.umlio.SequenceDiagramTestConstants import EXPECTED_SD_INSTANCES_XML
from tests.umlio.SequenceDiagramTestConstants import EXPECTED_SD_MESSAGES_XML
from tests.umlio.SequenceDiagramTestConstants import MESSAGE_MODEL_ID
from tests.umlio.SequenceDiagramTestConstants import MESSAGE_PLACE_ORDER_ID
from tests.umlio.SequenceDiagramTestConstants import MESSAGE_TEXT
from tests.umlio.SequenceDiagramTestConstants import MESSAGE_TIME_STEP
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_MODEL_ID


class TestXmlSDMessagesToUmlSDMessages(UnitTestBaseW):
    """
    Unit tests verifying deserialization of UmlSDMessage elements.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        OGLInitialize()

    def tearDown(self):
        super().tearDown()

    def testDeserializeSDMessages(self):
        instanceRoot:         Element                        = parse(EXPECTED_SD_INSTANCES_XML)
        instanceDiagram:      Element                        = instanceRoot.UMLDiagram
        instanceDeserializer: XmlSDInstancesToUmlSDInstances = XmlSDInstancesToUmlSDInstances()
        umlSDInstances:       UmlSDInstances                 = instanceDeserializer.deserialize(umlDiagramElement=instanceDiagram)

        messageRoot:         Element                      = parse(EXPECTED_SD_MESSAGES_XML)
        messageDiagram:      Element                      = messageRoot.UMLDiagram
        messageDeserializer: XmlSDMessagesToUmlSDMessages = XmlSDMessagesToUmlSDMessages()
        umlSDMessages:       UmlSDMessages                = messageDeserializer.deserialize(
            umlDiagramElement=messageDiagram,
            umlSDInstances=umlSDInstances
        )

        self.assertEqual(1, len(umlSDMessages), 'Expected 1 deserialized UmlSDMessage shape')

        placeOrderMessage: UmlSDMessage = umlSDMessages[0]
        self.assertEqual(MESSAGE_PLACE_ORDER_ID, placeOrderMessage.id)
        self.assertEqual(MESSAGE_MODEL_ID, placeOrderMessage.sdMessage.id)
        self.assertEqual(MESSAGE_TEXT, placeOrderMessage.sdMessage.message)
        self.assertEqual(MESSAGE_TEXT, placeOrderMessage.messageLabel.label)
        self.assertEqual(SDMessageType.SYNCHRONOUS, placeOrderMessage.messageType)
        self.assertEqual(MESSAGE_TIME_STEP, placeOrderMessage.fromY)
        self.assertEqual(MESSAGE_TIME_STEP, placeOrderMessage.toY)

        self.assertIsNotNone(placeOrderMessage.sdMessage.source, 'Source instance should be linked')
        self.assertEqual(CUSTOMER_MODEL_ID, placeOrderMessage.sdMessage.source.id)

        self.assertIsNotNone(placeOrderMessage.sdMessage.destination, 'Destination instance should be linked')
        self.assertEqual(ORDER_SERVICE_MODEL_ID, placeOrderMessage.sdMessage.destination.id)

    def testDeserializeEmptySDMessages(self):
        root:                Element                      = parse(EMPTY_SD_DIAGRAM_XML)
        diagram:             Element                      = root.UMLDiagram
        umlSDInstances:      UmlSDInstances               = UmlSDInstances([])
        messageDeserializer: XmlSDMessagesToUmlSDMessages = XmlSDMessagesToUmlSDMessages()
        umlSDMessages:       UmlSDMessages                = messageDeserializer.deserialize(
            umlDiagramElement=diagram,
            umlSDInstances=umlSDInstances
        )

        self.assertEqual(0, len(umlSDMessages), 'Expected 0 deserialized UmlSDMessage shapes for empty diagram')


def suite() -> TestSuite:
    testSuite: TestSuite = defaultTestLoader.loadTestsFromTestCase(TestXmlSDMessagesToUmlSDMessages)
    return testSuite


if __name__ == '__main__':
    unitTestMain()
