
from typing import cast

from pathlib import Path

from wx.lib.ogl import OGLInitialize

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from umlshapes.IApplicationAdapter import IApplicationAdapter
from umlshapes.frames.UmlClassDiagramFrame import CreateLollipopCallback
from umlshapes.frames.UmlClassDiagramFrame import UmlClassDiagramFrame
from umlshapes.preferences.UmlPreferences import UmlPreferences

from tests.RelationshipCreator import BASE_CLASS_PYUT_ID
from tests.RelationshipCreator import BASE_UML_CLASS_ID
from tests.RelationshipCreator import BASE_UML_CLASS_NAME
from tests.RelationshipCreator import SUBCLASS_PYUT_ID
from tests.RelationshipCreator import SUBCLASS_UML_CLASS_ID
from tests.RelationshipCreator import SUBCLASS_UML_CLASS_NAME

from tests.RelationshipCreator import SOURCE_PYUT_CLASS_ID as INT_SOURCE_PYUT_CLASS_ID
from tests.RelationshipCreator import DESTINATION_PYUT_CLASS_ID as INT_DESTINATION_PYUT_CLASS_ID

from tests.RelationshipCreator import SOURCE_UML_CLASS_ID
from tests.RelationshipCreator import DESTINATION_UML_CLASS_ID
from tests.RelationshipCreator import UML_LINK_CANONICAL_MONIKER

from umlio.IOTypes import UmlDiagramTitle
from umlio.IOTypes import UmlDiagramType

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from tests.RelationshipCreator import CreatedAssociation
from tests.RelationshipCreator import RelationshipCreator

from umlio.IOTypes import UmlDiagram

from umlio.UmlShapesToXml import UmlShapesToXml

from unittest import TestSuite
from unittest import main as unitTestMain

SOURCE_PYUT_CLASS_ID:      str = str(INT_SOURCE_PYUT_CLASS_ID)
DESTINATION_PYUT_CLASS_ID: str = str(INT_DESTINATION_PYUT_CLASS_ID)


EXPECTED_BARE_ASSOCIATION_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram type="Class Diagram" title="Bare Association Class Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'        <UmlClass id="{SOURCE_UML_CLASS_ID}" width="150" height="75" x="100" y="100">\n'
    f'            <PyutClass id="{SOURCE_PYUT_CLASS_ID}" name="GeneratedClass-0" displayMethods="True" displayParameters="Unspecified" displayConstructor="Unspecified" displayDunderMethods="Unspecified" displayFields="True" displayStereotype="True" fileName="" description="" />\n'
    '        </UmlClass>\n'
    f'        <UmlClass id="{DESTINATION_UML_CLASS_ID}" width="150" height="75" x="200" y="300">\n'
    f'            <PyutClass id="{DESTINATION_PYUT_CLASS_ID}" name="GeneratedClass-1" displayMethods="True" displayParameters="Unspecified" displayConstructor="Unspecified" displayDunderMethods="Unspecified" displayFields="True" displayStereotype="True" fileName="" description="" />\n'
    '        </UmlClass>\n'
    f'        <UmlLink id="{UML_LINK_CANONICAL_MONIKER}" fromX="194" fromY="174" toX="256" toY="300" spline="False">\n'
    '            <AssociationName deltaX="0" deltaY="0" />\n'
    '            <SourceCardinality deltaX="0" deltaY="0" />\n'
    '            <DestinationCardinality deltaX="0" deltaY="0" />\n'
    f'            <PyutLink name="Association-0" type="ASSOCIATION" sourceId="{SOURCE_PYUT_CLASS_ID}" destinationId="{DESTINATION_PYUT_CLASS_ID}" bidirectional="False" sourceCardinalityValue="src Card" destinationCardinalityValue="dst Card" />\n'
    '        </UmlLink>\n'
    '    </UMLDiagram>\n'
    '</UmlProject>'
)

EXPECTED_INHERITANCE_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram type="Class Diagram" title="Inheritance Class Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'        <UmlClass id="{SUBCLASS_UML_CLASS_ID}" width="150" height="75" x="200" y="300">\n'
    f'            <PyutClass id="{SUBCLASS_PYUT_ID}" name="{SUBCLASS_UML_CLASS_NAME}" displayMethods="True" displayParameters="Unspecified" displayConstructor="Unspecified" displayDunderMethods="Unspecified" displayFields="True" displayStereotype="True" fileName="" description="" />\n'
    '        </UmlClass>\n'
    f'        <UmlClass id="{BASE_UML_CLASS_ID}" width="150" height="75" x="100" y="100">\n'
    f'            <PyutClass id="{BASE_CLASS_PYUT_ID}" name="{BASE_UML_CLASS_NAME}" displayMethods="True" displayParameters="Unspecified" displayConstructor="Unspecified" displayDunderMethods="Unspecified" displayFields="True" displayStereotype="True" fileName="" description="" />\n'
    '        </UmlClass>\n'
    f'        <UmlLink id="{UML_LINK_CANONICAL_MONIKER}" fromX="248" fromY="300" toX="190" toY="174" spline="False">\n'
    '            <LineControlPoint x="100" y="100" />\n'
    '            <LineControlPoint x="200" y="200" />\n'
    '            <PyutLink name="" type="INHERITANCE" sourceId="111" destinationId="999" bidirectional="False" sourceCardinalityValue="" destinationCardinalityValue="" />\n'
    '        </UmlLink>\n'
    '    </UMLDiagram>\n'
    '</UmlProject>'
)

EXPECTED_INTERFACE_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram type="Class Diagram" title="Interface Class Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    '        <UmlClass id="valley.darkness.implementor" width="150" height="75" x="4444" y="4444">\n'
    '            <PyutClass id="4444" name="Implementor" displayMethods="True" displayParameters="Unspecified" displayConstructor="Unspecified" displayDunderMethods="Unspecified" displayFields="True" displayStereotype="True" fileName="" description="" />\n'
    '        </UmlClass>\n'
    '        <UmlClass id="card.carrying.interface" width="150" height="75" x="3333" y="3333">\n'
    '            <PyutClass id="2222" name="Interface" displayMethods="True" displayParameters="Unspecified" displayConstructor="Unspecified" displayDunderMethods="Unspecified" displayFields="True" displayStereotype="True" fileName="" description="" />\n'
    '        </UmlClass>\n'
    '        <UmlLink id="die.free.open.point" fromX="4481" fromY="4444" toX="3370" toY="3333" spline="False">\n'
    '            <LineControlPoint x="372" y="433" />\n'
    '            <LineControlPoint x="400" y="433" />\n'
    '            <PyutLink name="" type="INTERFACE" sourceId="4444" destinationId="2222" bidirectional="False" sourceCardinalityValue="" destinationCardinalityValue="" />\n'
    '        </UmlLink>\n'
    '    </UMLDiagram>\n'
    '</UmlProject>'
)


class TestUmlRelationships(UnitTestBaseW):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 24 June 2025
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        OGLInitialize()
        self._preferences: UmlPreferences = UmlPreferences()

        self._diagramFrame = UmlClassDiagramFrame(
            parent=self._topLevelWindow,
            applicationAdapter=cast(IApplicationAdapter, None),
            createLollipopCallback=cast(CreateLollipopCallback, None)
        )

        self._relationShipCreator: RelationshipCreator = RelationshipCreator(diagramFrame=self._diagramFrame)

    def tearDown(self):
        super().tearDown()

    def testBareAssociation(self):

        self._runAssociationTest(
            linkType=PyutLinkType.ASSOCIATION,
            fileName='Association.xml',
            diagramName='Bare Association Class Diagram',
            failMessage='Association serialization changed',
            expectedXml=EXPECTED_BARE_ASSOCIATION_XML
        )

    def testInheritance(self):

        self._runAssociationTest(
            linkType=PyutLinkType.INHERITANCE,
            fileName='Inheritance.xml',
            diagramName='Inheritance Class Diagram',
            failMessage='Inheritance serialization changed',
            expectedXml=EXPECTED_INHERITANCE_XML
        )

    def testInterface(self):
        self._runAssociationTest(
            linkType=PyutLinkType.INTERFACE,
            fileName='Interface.xml',
            diagramName='Interface Class Diagram',
            failMessage='Interface serialization changed',
            expectedXml=EXPECTED_INTERFACE_XML
        )

    def _runAssociationTest(self, linkType: PyutLinkType, fileName: str, diagramName: str, failMessage: str, expectedXml: str):
        """

        Args:
            linkType:
            fileName:
            diagramName:
            failMessage:
            expectedXml:
        """
        umlShapesToXml:      UmlShapesToXml = self._createXmlCreator()
        associationsDiagram: UmlDiagram     = self._createUmlDiagram(UmlDiagramType.CLASS_DIAGRAM, diagramName)

        createdAssociation: CreatedAssociation = self._relationShipCreator.createRelationship(linkType)

        associationsDiagram.umlClasses.append(createdAssociation.sourceUmlClass)
        associationsDiagram.umlClasses.append(createdAssociation.destinationUmlClass)
        associationsDiagram.umlLinks.append(createdAssociation.association)

        umlShapesToXml.serialize(umlDiagram=associationsDiagram)

        associationXML: str = umlShapesToXml.xml

        self.logger.debug(f'{associationXML=}')
        self._debugWriteToFile(fileName, xml=associationXML)

        self.maxDiff = None
        self.assertEqual(expectedXml, associationXML, failMessage)

    def _createXmlCreator(self) -> UmlShapesToXml:

        umlShapesToXml: UmlShapesToXml = UmlShapesToXml(projectCodePath=Path('/users/hasii'))
        return umlShapesToXml

    def _createUmlDiagram(self, diagramType: UmlDiagramType, diagramTitle: str) -> UmlDiagram:

        umlDiagram: UmlDiagram  = UmlDiagram()
        umlDiagram.diagramType  = diagramType
        umlDiagram.diagramTitle = UmlDiagramTitle(diagramTitle)

        return umlDiagram

    def _debugWriteToFile(self, fileName: str, xml: str):

        p: Path = Path(f'/tmp/{fileName}')

        p.write_text(xml)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUmlRelationships))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
