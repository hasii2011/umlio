
from unittest import defaultTestLoader
from unittest import TestSuite
from unittest import main as unitTestMain

from untangle import Element
from untangle import parse

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from umlshapes.lib.ogl import OGLInitialize
from umlshapes.sd.SDFragmentOperator import SDFragmentOperator
from umlshapes.sd.UmlSDCombinedFragment import UmlSDCombinedFragment

from umlio.IOTypes import UmlSDCombinedFragments
from umlio.deserializer.XmlSDFragmentsToUmlSDCombinedFragments import XmlSDFragmentsToUmlSDCombinedFragments

from tests.umlio.SequenceDiagramTestConstants import EMPTY_SD_DIAGRAM_XML
from tests.umlio.SequenceDiagramTestConstants import EXPECTED_SD_COMBINED_FRAGMENTS_XML
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_ALT_ID
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_HEIGHT
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_OPERATOR
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_WIDTH
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_X
from tests.umlio.SequenceDiagramTestConstants import FRAGMENT_Y
from tests.umlio.SequenceDiagramTestConstants import OPERAND_1_END_Y
from tests.umlio.SequenceDiagramTestConstants import OPERAND_1_GUARD
from tests.umlio.SequenceDiagramTestConstants import OPERAND_1_START_Y
from tests.umlio.SequenceDiagramTestConstants import OPERAND_2_END_Y
from tests.umlio.SequenceDiagramTestConstants import OPERAND_2_GUARD
from tests.umlio.SequenceDiagramTestConstants import OPERAND_2_START_Y


class TestXmlSDFragmentsToUmlSDCombinedFragments(UnitTestBaseW):
    """
    Unit tests verifying deserialization of UmlSDCombinedFragment elements.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        OGLInitialize()

    def testEmptyDiagramDeserialization(self):
        root:                 Element                               = parse(EMPTY_SD_DIAGRAM_XML)
        diagramElement:       Element                               = root.UMLDiagram
        deserializer:         XmlSDFragmentsToUmlSDCombinedFragments = XmlSDFragmentsToUmlSDCombinedFragments()
        deserializedFragments: UmlSDCombinedFragments               = deserializer.deserialize(
            umlDiagramElement=diagramElement
        )

        self.assertEqual(0, len(deserializedFragments), 'Expected 0 fragments for empty diagram')

    def testCombinedFragmentDeserialization(self):
        root:                 Element                               = parse(EXPECTED_SD_COMBINED_FRAGMENTS_XML)
        diagramElement:       Element                               = root.UMLDiagram
        deserializer:         XmlSDFragmentsToUmlSDCombinedFragments = XmlSDFragmentsToUmlSDCombinedFragments()
        deserializedFragments: UmlSDCombinedFragments               = deserializer.deserialize(
            umlDiagramElement=diagramElement
        )

        self.assertEqual(1, len(deserializedFragments), 'Expected 1 combined fragment deserialized')

        fragment: UmlSDCombinedFragment = deserializedFragments[0]
        self.assertEqual(FRAGMENT_ALT_ID, fragment.id)
        self.assertEqual(SDFragmentOperator(FRAGMENT_OPERATOR), fragment.operator)
        self.assertEqual(FRAGMENT_WIDTH, fragment.size.width)
        self.assertEqual(FRAGMENT_HEIGHT, fragment.size.height)
        self.assertEqual(FRAGMENT_X, fragment.position.x)
        self.assertEqual(FRAGMENT_Y, fragment.position.y)

        self.assertEqual(2, len(fragment.operands), 'Expected 2 operands')

        operand1 = fragment.operands[0]
        self.assertEqual(OPERAND_1_GUARD, operand1.guard)
        self.assertEqual(OPERAND_1_START_Y, operand1.startTimeStep)
        self.assertEqual(OPERAND_1_END_Y, operand1.endTimeStep)

        operand2 = fragment.operands[1]
        self.assertEqual(OPERAND_2_GUARD, operand2.guard)
        self.assertEqual(OPERAND_2_START_Y, operand2.startTimeStep)
        self.assertEqual(OPERAND_2_END_Y, operand2.endTimeStep)


def suite() -> TestSuite:
    testSuite: TestSuite = defaultTestLoader.loadTestsFromTestCase(TestXmlSDFragmentsToUmlSDCombinedFragments)
    return testSuite


if __name__ == '__main__':
    unitTestMain()
