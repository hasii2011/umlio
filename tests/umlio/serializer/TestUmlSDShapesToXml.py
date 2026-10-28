
from typing import Optional

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App
from wx import Frame

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import indent as xmlIndent
from xml.etree.ElementTree import tostring as xmlToString

from umlmodel.SDInstance import SDInstance
from umlmodel.SDMessage import SDMessage

from umlshapes.frames.SequenceDiagramFrame import SequenceDiagramFrame
from umlshapes.lib.ogl import OGLInitialize
from umlshapes.pubsubengine.IUmlPubSubEngine import IUmlPubSubEngine
from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine
from umlshapes.sd.SDMessageType import SDMessageType
from umlshapes.sd.UmlSDInstance import UmlSDInstance
from umlshapes.sd.UmlSDMessage import UmlSDMessage
from umlshapes.types.UmlPosition import UmlPosition

from umlio.IOTypes import UmlDocumentType
from umlio.IOTypes import UmlSDInstances
from umlio.IOTypes import UmlSDMessages
from umlio.serializer.UmlSDInstancesToXml import UmlSDInstancesToXml
from umlio.serializer.UmlSDMessagesToXml import UmlSDMessagesToXml
from umlio.XMLConstants import XmlConstants

from tests.umlio.UmlIOBaseTest import UmlIOBaseTest

CUSTOMER_INSTANCE_ID:        str = 'customer.instance'
ORDER_SERVICE_INSTANCE_ID:   str = 'orderservice.instance'
MESSAGE_PLACE_ORDER_ID:      str = 'msg.placeorder'

CUSTOMER_MODEL_ID:           str = 'inst-001'
ORDER_SERVICE_MODEL_ID:      str = 'inst-002'
MESSAGE_MODEL_ID:            str = 'sdmsg-001'

CUSTOMER_INSTANCE_NAME:      str = 'customer:Customer'
ORDER_SERVICE_INSTANCE_NAME: str = 'orderService:OrderService'
MESSAGE_TEXT:                str = 'placeOrder(orderId)'

INSTANCE_Y:                  int = 60
CUSTOMER_INSTANCE_X:         int = 120
CUSTOMER_INSTANCE_WIDTH:     int = 100

ORDER_SERVICE_INSTANCE_X:     int = 340
ORDER_SERVICE_INSTANCE_WIDTH: int = 120

DEFAULT_LIFELINE_LENGTH:     int = 400

MESSAGE_TIME_STEP:           int = 120

EXPECTED_SD_INSTANCES_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDInstance id="{CUSTOMER_INSTANCE_ID}" width="143" height="400" x="-71" y="-180" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{CUSTOMER_MODEL_ID}" instanceName="{CUSTOMER_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDInstance id="{ORDER_SERVICE_INSTANCE_ID}" width="186" height="400" x="-93" y="-180" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{ORDER_SERVICE_MODEL_ID}" instanceName="{ORDER_SERVICE_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    '</UMLDiagram>'
)

EXPECTED_SD_MESSAGES_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDMessage id="{MESSAGE_PLACE_ORDER_ID}" messageType="Synchronous Message">\n'
    f'        <ModelSDMessage id="{MESSAGE_MODEL_ID}" message="{MESSAGE_TEXT}" sourceTime="{MESSAGE_TIME_STEP}" destinationTime="{MESSAGE_TIME_STEP}" sourceId="{CUSTOMER_MODEL_ID}" destinationId="{ORDER_SERVICE_MODEL_ID}" />\n'
    '    </UmlSDMessage>\n'
    '</UMLDiagram>'
)

EXPECTED_SEQUENCE_DIAGRAM_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDInstance id="{CUSTOMER_INSTANCE_ID}" width="143" height="400" x="-71" y="-180" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{CUSTOMER_MODEL_ID}" instanceName="{CUSTOMER_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDInstance id="{ORDER_SERVICE_INSTANCE_ID}" width="186" height="400" x="-93" y="-180" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{ORDER_SERVICE_MODEL_ID}" instanceName="{ORDER_SERVICE_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDMessage id="{MESSAGE_PLACE_ORDER_ID}" messageType="Synchronous Message">\n'
    f'        <ModelSDMessage id="{MESSAGE_MODEL_ID}" message="{MESSAGE_TEXT}" sourceTime="{MESSAGE_TIME_STEP}" destinationTime="{MESSAGE_TIME_STEP}" sourceId="{CUSTOMER_MODEL_ID}" destinationId="{ORDER_SERVICE_MODEL_ID}" />\n'
    '    </UmlSDMessage>\n'
    '</UMLDiagram>'
)


class TestUmlSDShapesToXml(UmlIOBaseTest):
    """
    Unit tests for sequence diagram serializers comparing against golden XML representations.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        OGLInitialize()

        self._dummyParent: Frame = Frame(None)
        self._pubSubEngine: IUmlPubSubEngine = UmlPubSubEngine()
        self._diagramFrame: SequenceDiagramFrame = SequenceDiagramFrame(
            parent=self._dummyParent,
            umlPubSubEngine=self._pubSubEngine
        )

    def tearDown(self):
        if self._dummyParent is not None:
            self._dummyParent.Destroy()
        super().tearDown()

    def testSerializeSDInstances(self):
        umlSDInstances: UmlSDInstances = self._createTestSDInstances()

        documentTop: Element = self._createDiagramElement()
        serializer: UmlSDInstancesToXml = UmlSDInstancesToXml()
        serializer.serialize(documentTop=documentTop, umlSDInstances=umlSDInstances)

        actualXml: str = self._toPrettyXml(element=documentTop)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SD_INSTANCES_XML, actualXml, 'SD Instances serialization changed')

    def testSerializeSDMessages(self):
        umlSDMessages: UmlSDMessages = self._createTestSDMessages()

        documentTop: Element = self._createDiagramElement()
        serializer: UmlSDMessagesToXml = UmlSDMessagesToXml()
        serializer.serialize(documentTop=documentTop, umlSDMessages=umlSDMessages)

        actualXml: str = self._toPrettyXml(element=documentTop)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SD_MESSAGES_XML, actualXml, 'SD Messages serialization changed')

    def testSerializeSequenceDiagramFull(self):
        umlSDInstances: UmlSDInstances = self._createTestSDInstances()
        umlSDMessages: UmlSDMessages = self._createTestSDMessages()

        documentTop: Element = self._createDiagramElement()

        instancesSerializer: UmlSDInstancesToXml = UmlSDInstancesToXml()
        instancesSerializer.serialize(documentTop=documentTop, umlSDInstances=umlSDInstances)

        messagesSerializer: UmlSDMessagesToXml = UmlSDMessagesToXml()
        messagesSerializer.serialize(documentTop=documentTop, umlSDMessages=umlSDMessages)

        actualXml: str = self._toPrettyXml(element=documentTop)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SEQUENCE_DIAGRAM_XML, actualXml, 'Sequence Diagram full serialization changed')

    def _createTestSDInstances(self) -> UmlSDInstances:
        sdInstance1: SDInstance = SDInstance(instanceName=CUSTOMER_INSTANCE_NAME)
        sdInstance1.id = CUSTOMER_MODEL_ID

        sdInstance2: SDInstance = SDInstance(instanceName=ORDER_SERVICE_INSTANCE_NAME)
        sdInstance2.id = ORDER_SERVICE_MODEL_ID

        umlSDInstance1: UmlSDInstance = UmlSDInstance(
            sdInstance=sdInstance1,
            diagramFrame=self._diagramFrame,
            umlPubSubEngine=self._pubSubEngine
        )
        umlSDInstance1.id = CUSTOMER_INSTANCE_ID
        umlSDInstance1.position = UmlPosition(x=CUSTOMER_INSTANCE_X, y=INSTANCE_Y)
        umlSDInstance1.setInstanceWidth(CUSTOMER_INSTANCE_WIDTH)
        umlSDInstance1.setLifeLineLength(DEFAULT_LIFELINE_LENGTH)

        umlSDInstance2: UmlSDInstance = UmlSDInstance(
            sdInstance=sdInstance2,
            diagramFrame=self._diagramFrame,
            umlPubSubEngine=self._pubSubEngine
        )
        umlSDInstance2.id = ORDER_SERVICE_INSTANCE_ID
        umlSDInstance2.position = UmlPosition(x=ORDER_SERVICE_INSTANCE_X, y=INSTANCE_Y)
        umlSDInstance2.setInstanceWidth(ORDER_SERVICE_INSTANCE_WIDTH)
        umlSDInstance2.setLifeLineLength(DEFAULT_LIFELINE_LENGTH)

        return UmlSDInstances([umlSDInstance1, umlSDInstance2])

    def _createTestSDMessages(self) -> UmlSDMessages:
        sdInstance1: SDInstance = SDInstance(instanceName=CUSTOMER_INSTANCE_NAME)
        sdInstance1.id = CUSTOMER_MODEL_ID

        sdInstance2: SDInstance = SDInstance(instanceName=ORDER_SERVICE_INSTANCE_NAME)
        sdInstance2.id = ORDER_SERVICE_MODEL_ID

        sdMessage1: SDMessage = SDMessage(
            message=MESSAGE_TEXT,
            src=sdInstance1,
            sourceY=MESSAGE_TIME_STEP,
            dst=sdInstance2,
            destinationY=MESSAGE_TIME_STEP
        )
        sdMessage1.id = MESSAGE_MODEL_ID

        umlSDMessage1: UmlSDMessage = UmlSDMessage(
            sdMessage=sdMessage1,
            umlPubSubEngine=self._pubSubEngine,
            messageType=SDMessageType.SYNCHRONOUS
        )
        umlSDMessage1.id = MESSAGE_PLACE_ORDER_ID

        return UmlSDMessages([umlSDMessage1])

    def _createDiagramElement(self) -> Element:
        diagramAttributes = {
            XmlConstants.ATTRIBUTE_DOCUMENT_TYPE:    UmlDocumentType.SEQUENCE_DOCUMENT.value,
            XmlConstants.ATTRIBUTE_TITLE:            'Order Processing',
            XmlConstants.ATTRIBUTE_SCROLL_POSITION_X: '1',
            XmlConstants.ATTRIBUTE_SCROLL_POSITION_Y: '1',
            XmlConstants.ATTRIBUTE_PIXELS_PER_UNIT_X: '1',
            XmlConstants.ATTRIBUTE_PIXELS_PER_UNIT_Y: '1',
        }
        return Element(XmlConstants.ELEMENT_UML_DIAGRAM, attrib=diagramAttributes)

    def _toPrettyXml(self, element: Element) -> str:
        xmlIndent(element, space='    ', level=0)
        return xmlToString(element, encoding='iso-8859-1', xml_declaration=True).decode('utf-8')


def suite() -> TestSuite:
    testSuite: TestSuite = TestSuite()
    testSuite.addTest(TestUmlSDShapesToXml('testSerializeSDInstances'))
    testSuite.addTest(TestUmlSDShapesToXml('testSerializeSDMessages'))
    testSuite.addTest(TestUmlSDShapesToXml('testSerializeSequenceDiagramFull'))
    return testSuite


if __name__ == '__main__':
    unitTestMain()
