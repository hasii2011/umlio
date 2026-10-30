
from unittest import defaultTestLoader
from unittest import TestSuite
from unittest import main as unitTestMain

from untangle import Element
from untangle import parse

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from umlshapes.frames.SequenceDiagramFrame import SequenceDiagramFrame
from umlshapes.lib.ogl import OGLInitialize
from umlshapes.pubsubengine.IUmlPubSubEngine import IUmlPubSubEngine
from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine
from umlshapes.sd.UmlSDInstance import UmlSDInstance

from umlio.IOTypes import UmlSDInstances
from umlio.deserializer.XmlSDInstancesToUmlSDInstances import XmlSDInstancesToUmlSDInstances

from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_INSTANCE_ID
from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_INSTANCE_NAME
from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_INSTANCE_X
from tests.umlio.SequenceDiagramTestConstants import CUSTOMER_MODEL_ID
from tests.umlio.SequenceDiagramTestConstants import DEFAULT_LIFELINE_LENGTH
from tests.umlio.SequenceDiagramTestConstants import EMPTY_SD_DIAGRAM_XML
from tests.umlio.SequenceDiagramTestConstants import EXPECTED_SD_INSTANCES_XML
from tests.umlio.SequenceDiagramTestConstants import INSTANCE_Y
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_INSTANCE_ID
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_INSTANCE_NAME
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_INSTANCE_X
from tests.umlio.SequenceDiagramTestConstants import ORDER_SERVICE_MODEL_ID


class TestXmlSDInstancesToUmlSDInstances(UnitTestBaseW):
    """
    Unit tests verifying deserialization of UmlSDInstance elements.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        OGLInitialize()

        self._pubSubEngine: IUmlPubSubEngine     = UmlPubSubEngine()
        self._diagramFrame: SequenceDiagramFrame = SequenceDiagramFrame(
            parent=self._topLevelWindow,
            umlPubSubEngine=self._pubSubEngine
        )

    def tearDown(self):
        super().tearDown()

    def testDeserializeSDInstances(self):
        root:           Element                        = parse(EXPECTED_SD_INSTANCES_XML)
        diagram:        Element                        = root.UMLDiagram
        deserializer:   XmlSDInstancesToUmlSDInstances = XmlSDInstancesToUmlSDInstances(
            diagramFrame=self._diagramFrame,
            umlPubSubEngine=self._pubSubEngine
        )
        umlSDInstances: UmlSDInstances                 = deserializer.deserialize(umlDiagramElement=diagram)

        self.assertEqual(2, len(umlSDInstances), 'Expected 2 deserialized UmlSDInstance shapes')

        customerInstance: UmlSDInstance = umlSDInstances[0]
        self.assertEqual(CUSTOMER_INSTANCE_ID, customerInstance.id)
        self.assertEqual(CUSTOMER_MODEL_ID, customerInstance.sdInstance.id)
        self.assertEqual(CUSTOMER_INSTANCE_NAME, customerInstance.sdInstance.instanceName)
        self.assertEqual(CUSTOMER_INSTANCE_X, customerInstance.position.x)
        self.assertEqual(INSTANCE_Y, customerInstance.position.y)
        self.assertEqual(DEFAULT_LIFELINE_LENGTH, customerInstance.getLifeLineLength())

        orderServiceInstance: UmlSDInstance = umlSDInstances[1]
        self.assertEqual(ORDER_SERVICE_INSTANCE_ID, orderServiceInstance.id)
        self.assertEqual(ORDER_SERVICE_MODEL_ID, orderServiceInstance.sdInstance.id)
        self.assertEqual(ORDER_SERVICE_INSTANCE_NAME, orderServiceInstance.sdInstance.instanceName)
        self.assertEqual(ORDER_SERVICE_INSTANCE_X, orderServiceInstance.position.x)
        self.assertEqual(INSTANCE_Y, orderServiceInstance.position.y)
        self.assertEqual(DEFAULT_LIFELINE_LENGTH, orderServiceInstance.getLifeLineLength())

    def testDeserializeEmptySDInstances(self):
        root:           Element                        = parse(EMPTY_SD_DIAGRAM_XML)
        diagram:        Element                        = root.UMLDiagram
        deserializer:   XmlSDInstancesToUmlSDInstances = XmlSDInstancesToUmlSDInstances(
            diagramFrame=self._diagramFrame,
            umlPubSubEngine=self._pubSubEngine
        )
        umlSDInstances: UmlSDInstances                 = deserializer.deserialize(umlDiagramElement=diagram)

        self.assertEqual(0, len(umlSDInstances), 'Expected 0 deserialized UmlSDInstance shapes for empty diagram')


def suite() -> TestSuite:
    testSuite: TestSuite = defaultTestLoader.loadTestsFromTestCase(TestXmlSDInstancesToUmlSDInstances)
    return testSuite


if __name__ == '__main__':
    unitTestMain()
