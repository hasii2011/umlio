
from typing import cast

from pathlib import Path

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine
from umlshapes.frames.ClassDiagramFrame import ClassDiagramFrame
from umlshapes.frames.ClassDiagramFrame import CreateLollipopCallback

from umlshapes.preferences.UmlPreferences import UmlPreferences

from tests.LinkCreator import BASE_CLASS_PYUT_ID
from tests.LinkCreator import BASE_UML_CLASS_ID
from tests.LinkCreator import BASE_UML_CLASS_NAME
from tests.LinkCreator import CANONICAl_LOLLIPOP_NAME
from tests.LinkCreator import IMPLEMENTING_UML_CLASS_ID
from tests.LinkCreator import IMPLEMENTING_UML_CLASS_NAME
from tests.LinkCreator import PYUT_INTERFACE_CANONICAL_ID
from tests.LinkCreator import SUBCLASS_PYUT_ID
from tests.LinkCreator import SUBCLASS_UML_CLASS_ID
from tests.LinkCreator import SUBCLASS_UML_CLASS_NAME

from tests.LinkCreator import SOURCE_PYUT_CLASS_ID as INT_SOURCE_PYUT_CLASS_ID
from tests.LinkCreator import DESTINATION_PYUT_CLASS_ID as INT_DESTINATION_PYUT_CLASS_ID

from tests.LinkCreator import SOURCE_UML_CLASS_ID
from tests.LinkCreator import DESTINATION_UML_CLASS_ID
from tests.LinkCreator import UML_LINK_CANONICAL_MONIKER

from umlio.IOTypes import UmlDocumentTitle
from umlio.IOTypes import UmlDocumentType

from tests.LinkCreator import CreatedLink
from tests.LinkCreator import LinkCreator

from umlshapes.lib.ogl import OGLInitialize

from umlio.IOTypes import UmlDocument

from umlio.serializer.UmlShapesToXml import UmlShapesToXml

from unittest import TestSuite
from unittest import main as unitTestMain

SOURCE_PYUT_CLASS_ID:      str = str(INT_SOURCE_PYUT_CLASS_ID)
DESTINATION_PYUT_CLASS_ID: str = str(INT_DESTINATION_PYUT_CLASS_ID)


EXPECTED_BARE_ASSOCIATION_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram documentType="Class Document" title="Bare Association Class Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
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
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram documentType="Class Document" title="Inheritance Class Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
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
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram documentType="Class Document" title="Interface Class Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
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

EXPECTED_LOLLIPOP_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    f'<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    f'    <UMLDiagram documentType="Class Document" title="Lollipop Class Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'        <UmlClass id="valley.darkness.implementor" width="150" height="75" x="3333" y="3333">\n'
    f'            <PyutClass id="4444" name="{IMPLEMENTING_UML_CLASS_NAME}" displayMethods="True" displayParameters="Unspecified" displayConstructor="Unspecified" displayDunderMethods="Unspecified" displayFields="True" displayStereotype="True" fileName="" description="" />\n'
    f'        </UmlClass>\n'
    f'        <UmlLollipopInterface lineCentum="0.1" attachmentSide="Right" attachedToId="{IMPLEMENTING_UML_CLASS_ID}">\n'
    f'            <PyutInterface id="{PYUT_INTERFACE_CANONICAL_ID}" name="{CANONICAl_LOLLIPOP_NAME}" description="">\n'
    f'                <Implementor implementingClassName="{IMPLEMENTING_UML_CLASS_NAME}" />\n'
    f'            </PyutInterface>\n'
    f'        </UmlLollipopInterface>\n'
    f'    </UMLDiagram>\n'
    f'</UmlProject>'

)


class TestUmlRelationshipsToXml(UnitTestBaseW):
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
        self._umlPubSubEngine: UmlPubSubEngine = UmlPubSubEngine()
        self._preferences: UmlPreferences = UmlPreferences()

        self._diagramFrame = ClassDiagramFrame(
            parent=self._topLevelWindow,
            umlPubSubEngine=self._umlPubSubEngine,
            createLollipopCallback=cast(CreateLollipopCallback, None)
        )

        self._linkCreator: LinkCreator = LinkCreator(diagramFrame=self._diagramFrame)

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

        umlShapesToXml:      UmlShapesToXml = self._createXmlCreator()
        inheritanceDiagram: UmlDocument     = self._createUmlDiagram(UmlDocumentType.CLASS_DOCUMENT, 'Inheritance Class Diagram')

        createdLink: CreatedLink = self._linkCreator.createUmlInheritance()

        inheritanceDiagram.umlClasses.append(createdLink.sourceUmlClass)
        inheritanceDiagram.umlClasses.append(createdLink.destinationUmlClass)
        inheritanceDiagram.umlLinks.append(createdLink.association)

        umlShapesToXml.serialize(umlDiagram=inheritanceDiagram)

        inheritanceXML: str = umlShapesToXml.xml

        self._debugWriteToFile('Inheritance.xml', xml=inheritanceXML)

        self.maxDiff = None
        self.assertEqual(EXPECTED_INHERITANCE_XML, inheritanceXML, 'Inheritance serialization changed')

    def testInterface(self):
        umlShapesToXml:   UmlShapesToXml = self._createXmlCreator()
        interfaceDiagram: UmlDocument    = self._createUmlDiagram(UmlDocumentType.CLASS_DOCUMENT, 'Interface Class Diagram')
        createdLink: CreatedLink = self._linkCreator.createUmlInterface()

        interfaceDiagram.umlClasses.append(createdLink.sourceUmlClass)
        interfaceDiagram.umlClasses.append(createdLink.destinationUmlClass)
        interfaceDiagram.umlLinks.append(createdLink.association)

        umlShapesToXml.serialize(umlDiagram=interfaceDiagram)

        interfaceXml: str = umlShapesToXml.xml

        self._debugWriteToFile('Interface.xml', xml=interfaceXml)

        self.maxDiff = None
        self.assertEqual(EXPECTED_INTERFACE_XML, interfaceXml, 'Interface serialization changed')

    def testLollipop(self):
        umlShapesToXml:  UmlShapesToXml = self._createXmlCreator()
        lollipopDiagram: UmlDocument    = self._createUmlDiagram(UmlDocumentType.CLASS_DOCUMENT, 'Lollipop Class Diagram')

        umlLollipopInterface, implementingUmlClass = self._linkCreator.createLollipop()

        lollipopDiagram.umlClasses.append(implementingUmlClass)
        lollipopDiagram.umlLinks.append(umlLollipopInterface)
        umlShapesToXml.serialize(umlDiagram=lollipopDiagram)

        lollipopXml: str = umlShapesToXml.xml

        self._debugWriteToFile('Lollipop.xml', xml=lollipopXml)

        self.maxDiff = None
        self.assertEqual(EXPECTED_LOLLIPOP_XML, lollipopXml, 'Lollipop serialization changed')

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
        associationsDiagram: UmlDocument     = self._createUmlDiagram(UmlDocumentType.CLASS_DOCUMENT, diagramName)

        createdLink: CreatedLink = self._linkCreator.createAssociation(linkType)

        if linkType == PyutLinkType.LOLLIPOP:
            umlLollipopInterface, implementingUmlClass = self._linkCreator.createLollipop()

            associationsDiagram.umlClasses.append(implementingUmlClass)
            associationsDiagram.umlLinks.append(umlLollipopInterface)
        else:
            associationsDiagram.umlClasses.append(createdLink.sourceUmlClass)
            associationsDiagram.umlClasses.append(createdLink.destinationUmlClass)
            associationsDiagram.umlLinks.append(createdLink.association)

        umlShapesToXml.serialize(umlDiagram=associationsDiagram)

        associationXML: str = umlShapesToXml.xml

        self.logger.debug(f'{associationXML=}')
        self._debugWriteToFile(fileName, xml=associationXML)

        self.maxDiff = None
        self.assertEqual(expectedXml, associationXML, failMessage)

    def _createXmlCreator(self) -> UmlShapesToXml:

        umlShapesToXml: UmlShapesToXml = UmlShapesToXml(projectFileName=Path(''), projectCodePath=Path('/users/hasii'))
        return umlShapesToXml

    def _createUmlDiagram(self, diagramType: UmlDocumentType, diagramTitle: str) -> UmlDocument:

        umlDiagram: UmlDocument  = UmlDocument()
        umlDiagram.documentType  = diagramType
        umlDiagram.documentTitle = UmlDocumentTitle(diagramTitle)

        return umlDiagram

    def _debugWriteToFile(self, fileName: str, xml: str):

        p: Path = Path(f'/tmp/{fileName}')

        p.write_text(xml)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUmlRelationshipsToXml))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
