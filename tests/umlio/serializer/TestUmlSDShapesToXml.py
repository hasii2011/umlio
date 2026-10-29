
from typing import Optional

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App
from wx import Frame

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import indent as xmlIndent
from xml.etree.ElementTree import tostring as xmlToString

from umlmodel.SDExecution import SDExecution
from umlmodel.SDInstance import SDInstance
from umlmodel.SDMessage import SDMessage

from umlshapes.frames.SequenceDiagramFrame import SequenceDiagramFrame
from umlshapes.lib.ogl import OGLInitialize
from umlshapes.pubsubengine.IUmlPubSubEngine import IUmlPubSubEngine
from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine
from umlshapes.sd.SDMessageType import SDMessageType
from umlshapes.sd.UmlSDInstance import UmlSDInstance
from umlshapes.sd.UmlSDMessage import UmlSDMessage
from umlshapes.sd.UmlSDExecution import UmlSDExecution
from umlshapes.types.UmlPosition import UmlPosition

from umlio.IOTypes import UmlDocumentType
from umlio.IOTypes import UmlSDInstances
from umlio.IOTypes import UmlSDMessages
from umlio.IOTypes import UmlSDExecutions
from umlio.serializer.UmlSDInstancesToXml import UmlSDInstancesToXml
from umlio.serializer.UmlSDMessagesToXml import UmlSDMessagesToXml
from umlio.serializer.UmlSDExecutionsToXml import UmlSDExecutionsToXml
from umlio.XMLConstants import XmlConstants

from tests.umlio.UmlIOBaseTest import UmlIOBaseTest

CUSTOMER_INSTANCE_ID:        str = 'customer.instance'
ORDER_SERVICE_INSTANCE_ID:   str = 'orderservice.instance'
MESSAGE_PLACE_ORDER_ID:      str = 'msg.placeorder'
EXECUTION_ORDER_SERVICE_ID:  str = 'exec.orderservice.1'

CUSTOMER_MODEL_ID:           str = 'inst-001'
ORDER_SERVICE_MODEL_ID:      str = 'inst-002'
MESSAGE_MODEL_ID:            str = 'sdmsg-001'
EXECUTION_MODEL_ID:          str = 'sdexec-001'

CUSTOMER_INSTANCE_NAME:      str = 'customer:Customer'
ORDER_SERVICE_INSTANCE_NAME: str = 'orderService:OrderService'
MESSAGE_TEXT:                str = 'placeOrder(orderId)'
EXECUTION_OPERATION_NAME:    str = 'placeOrder'

INSTANCE_Y:                  int = 60
CUSTOMER_INSTANCE_X:         int = 120
CUSTOMER_INSTANCE_WIDTH:     int = 100

ORDER_SERVICE_INSTANCE_X:     int = 340
ORDER_SERVICE_INSTANCE_WIDTH: int = 120

DEFAULT_LIFELINE_LENGTH:     int = 400

MESSAGE_TIME_STEP:           int = 120

EXECUTION_START_Y:           int = 120
EXECUTION_END_Y:             int = 260
EXECUTION_NESTING_LEVEL:     int = 0

EXPECTED_SD_INSTANCES_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDInstance id="{CUSTOMER_INSTANCE_ID}" width="{CUSTOMER_INSTANCE_WIDTH}" height="{DEFAULT_LIFELINE_LENGTH}" x="{CUSTOMER_INSTANCE_X}" y="{INSTANCE_Y}" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{CUSTOMER_MODEL_ID}" instanceName="{CUSTOMER_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDInstance id="{ORDER_SERVICE_INSTANCE_ID}" width="{ORDER_SERVICE_INSTANCE_WIDTH}" height="{DEFAULT_LIFELINE_LENGTH}" x="{ORDER_SERVICE_INSTANCE_X}" y="{INSTANCE_Y}" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
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

EXPECTED_SD_EXECUTIONS_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDExecution id="{EXECUTION_ORDER_SERVICE_ID}">\n'
    f'        <ModelSDExecution id="{EXECUTION_MODEL_ID}" instanceId="{ORDER_SERVICE_MODEL_ID}" startTime="{EXECUTION_START_Y}" endTime="{EXECUTION_END_Y}" nestingLevel="{EXECUTION_NESTING_LEVEL}" operation="{EXECUTION_OPERATION_NAME}" />\n'
    '    </UmlSDExecution>\n'
    '</UMLDiagram>'
)

EXPECTED_SEQUENCE_DIAGRAM_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDInstance id="{CUSTOMER_INSTANCE_ID}" width="{CUSTOMER_INSTANCE_WIDTH}" height="{DEFAULT_LIFELINE_LENGTH}" x="{CUSTOMER_INSTANCE_X}" y="{INSTANCE_Y}" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{CUSTOMER_MODEL_ID}" instanceName="{CUSTOMER_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDInstance id="{ORDER_SERVICE_INSTANCE_ID}" width="{ORDER_SERVICE_INSTANCE_WIDTH}" height="{DEFAULT_LIFELINE_LENGTH}" x="{ORDER_SERVICE_INSTANCE_X}" y="{INSTANCE_Y}" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{ORDER_SERVICE_MODEL_ID}" instanceName="{ORDER_SERVICE_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDMessage id="{MESSAGE_PLACE_ORDER_ID}" messageType="Synchronous Message">\n'
    f'        <ModelSDMessage id="{MESSAGE_MODEL_ID}" message="{MESSAGE_TEXT}" sourceTime="{MESSAGE_TIME_STEP}" destinationTime="{MESSAGE_TIME_STEP}" sourceId="{CUSTOMER_MODEL_ID}" destinationId="{ORDER_SERVICE_MODEL_ID}" />\n'
    '    </UmlSDMessage>\n'
    f'    <UmlSDExecution id="{EXECUTION_ORDER_SERVICE_ID}">\n'
    f'        <ModelSDExecution id="{EXECUTION_MODEL_ID}" instanceId="{ORDER_SERVICE_MODEL_ID}" startTime="{EXECUTION_START_Y}" endTime="{EXECUTION_END_Y}" nestingLevel="{EXECUTION_NESTING_LEVEL}" operation="{EXECUTION_OPERATION_NAME}" />\n'
    '    </UmlSDExecution>\n'
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

    def testSerializeSDExecutions(self):
        umlSDInstances: UmlSDInstances = self._createTestSDInstances()
        umlSDExecutions: UmlSDExecutions = self._createTestSDExecutions(umlSDInstances=umlSDInstances)

        documentTop: Element = self._createDiagramElement()
        serializer: UmlSDExecutionsToXml = UmlSDExecutionsToXml()
        serializer.serialize(documentTop=documentTop, umlSDExecutions=umlSDExecutions)

        actualXml: str = self._toPrettyXml(element=documentTop)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SD_EXECUTIONS_XML, actualXml, 'SD Executions serialization changed')

    def testSerializeSequenceDiagramFull(self):
        umlSDInstances: UmlSDInstances = self._createTestSDInstances()
        umlSDMessages: UmlSDMessages = self._createTestSDMessages()
        umlSDExecutions: UmlSDExecutions = self._createTestSDExecutions(umlSDInstances=umlSDInstances)

        documentTop: Element = self._createDiagramElement()

        instancesSerializer: UmlSDInstancesToXml = UmlSDInstancesToXml()
        instancesSerializer.serialize(documentTop=documentTop, umlSDInstances=umlSDInstances)

        messagesSerializer: UmlSDMessagesToXml = UmlSDMessagesToXml()
        messagesSerializer.serialize(documentTop=documentTop, umlSDMessages=umlSDMessages)

        executionsSerializer: UmlSDExecutionsToXml = UmlSDExecutionsToXml()
        executionsSerializer.serialize(documentTop=documentTop, umlSDExecutions=umlSDExecutions)

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
        umlSDInstance1.setInstanceWidth(CUSTOMER_INSTANCE_WIDTH)
        umlSDInstance1.setLifeLineLength(DEFAULT_LIFELINE_LENGTH)
        umlSDInstance1._size.SetWidth(CUSTOMER_INSTANCE_WIDTH)
        umlSDInstance1._size.SetHeight(DEFAULT_LIFELINE_LENGTH)
        umlSDInstance1.position = UmlPosition(x=CUSTOMER_INSTANCE_X, y=INSTANCE_Y)

        umlSDInstance2: UmlSDInstance = UmlSDInstance(
            sdInstance=sdInstance2,
            diagramFrame=self._diagramFrame,
            umlPubSubEngine=self._pubSubEngine
        )
        umlSDInstance2.id = ORDER_SERVICE_INSTANCE_ID
        umlSDInstance2.setInstanceWidth(ORDER_SERVICE_INSTANCE_WIDTH)
        umlSDInstance2.setLifeLineLength(DEFAULT_LIFELINE_LENGTH)
        umlSDInstance2._size.SetWidth(ORDER_SERVICE_INSTANCE_WIDTH)
        umlSDInstance2._size.SetHeight(DEFAULT_LIFELINE_LENGTH)
        umlSDInstance2.position = UmlPosition(x=ORDER_SERVICE_INSTANCE_X, y=INSTANCE_Y)

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

    def _createTestSDExecutions(self, umlSDInstances: UmlSDInstances) -> UmlSDExecutions:
        orderServiceInstance: UmlSDInstance = umlSDInstances[1]

        sdExecution1: SDExecution = SDExecution(
            instance=orderServiceInstance.sdInstance,
            startTime=EXECUTION_START_Y,
            endTime=EXECUTION_END_Y,
            nestingLevel=EXECUTION_NESTING_LEVEL,
            operation=EXECUTION_OPERATION_NAME
        )
        sdExecution1.id = EXECUTION_MODEL_ID

        umlSDExecution1: UmlSDExecution = UmlSDExecution(
            lifeLine=orderServiceInstance._umlSDLifeLine,
            startY=EXECUTION_START_Y,
            endY=EXECUTION_END_Y,
            nestingLevel=EXECUTION_NESTING_LEVEL,
            sdExecution=sdExecution1
        )
        umlSDExecution1.id = EXECUTION_ORDER_SERVICE_ID

        return UmlSDExecutions([umlSDExecution1])

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
    testSuite.addTest(TestUmlSDShapesToXml('testSerializeSDExecutions'))
    testSuite.addTest(TestUmlSDShapesToXml('testSerializeSequenceDiagramFull'))
    return testSuite


if __name__ == '__main__':
    unitTestMain()
