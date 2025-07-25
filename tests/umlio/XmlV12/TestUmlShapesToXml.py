
from typing import List
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from os import sep as osSep

from pathlib import Path

from random import choice

from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutParameter import PyutParameter
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutType import PyutType
from pyutmodelv2.PyutUseCase import PyutUseCase
from pyutmodelv2.enumerations.PyutDisplayParameters import PyutDisplayParameters
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility

from umlshapes.preferences.UmlPreferences import UmlPreferences

from umlshapes.shapes.UmlActor import UmlActor
from umlshapes.shapes.UmlClass import UmlClass
from umlshapes.shapes.UmlNote import UmlNote
from umlshapes.shapes.UmlText import UmlText
from umlshapes.shapes.UmlUseCase import UmlUseCase

from umlshapes.types.UmlDimensions import UmlDimensions
from umlshapes.types.UmlPosition import UmlPosition

from wx.lib.ogl import OGLInitialize

from umlio.IOTypes import UmlDocument
from umlio.IOTypes import UmlDocumentType

from umlio.serializer.UmlShapesToXml import UmlShapesToXml

from tests.umlio.UmlIOBaseTest import UmlIOBaseTest

EXPECTED_EMPTY_PROJECT: str = '<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<UmlProject fileName="." version="12.0" codePath="/users/hasii" />'

EXPECTED_EMPTY_DIAGRAM: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n    '
    '<UMLDiagram documentType="Not Set" title="" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1" />\n'
    '</UmlProject>'
)

EXPECTED_SINGLE_CLASS_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram documentType="Class Document" title="Unit Test Class Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    '        <UmlClass id="play.small.long.group" width="125" height="100" x="300" y="500">\n'
    '            <PyutClass id="0" name="ClassName1" displayMethods="True" displayParameters="Unspecified" displayConstructor="Unspecified" displayDunderMethods="Unspecified" displayFields="True" displayStereotype="True" fileName="" description="" />\n'
    '        </UmlClass>\n'
    '    </UMLDiagram>\n'
    '</UmlProject>'
)

EXPECTED_SINGLE_USE_CASE_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram documentType="Use Case Document" title="Use Case Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    '        <UmlUseCase id="remember.central.issue.child" width="125" height="100" x="300" y="500">\n'
    '            <PyutUseCase id="1" name="I am a lonely boy" fileName="" />\n'
    '        </UmlUseCase>\n'
    '    </UMLDiagram>\n'
    '</UmlProject>'
)

EXPECTED_SINGLE_ACTOR: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram documentType="Use Case Document" title="Use Case Actor Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    '        <UmlActor id="remember.central.issue.child" width="233" height="233" x="500" y="200">\n'
    '            <PyutActor id="0" name="LoboMalo" fileName="" />\n'
    '        </UmlActor>\n'
    '    </UMLDiagram>\n'
    '</UmlProject>'
)

EXPECTED_SINGLE_NOTE: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram documentType="Use Case Document" title="Uml Note Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    '        <UmlNote id="remember.the.Alamo" width="233" height="233" x="666" y="777">\n'
    '            <PyutNote id="777" content="I am the best MAGA Note" fileName="" />\n'
    '        </UmlNote>\n'
    '    </UMLDiagram>\n'
    '</UmlProject>'
)

EXPECTED_SINGLE_TEXT: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UmlProject fileName="." version="12.0" codePath="/users/hasii">\n'
    '    <UMLDiagram documentType="Class Document" title="Uml Text Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    '        <UmlText id="remember.the.Alamo" width="150" height="50" x="1024" y="768">\n'
    '            <PyutText id="1789" content="Soy el mejor texto americano" />\n'
    '        </UmlText>\n'
    '    </UMLDiagram>\n'
    '</UmlProject>'
)


class TestUmlShapesToXml(UmlIOBaseTest):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 19 June 2025
    """

    classCounter:     int  = 111
    methodCounter:    int  = 222
    parameterCounter: int  = 333
    fieldCounter:     int  = 444
    TEMPORARY_PATH:   Path = cast(Path, None)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        TestUmlShapesToXml.TEMPORARY_PATH = Path(f'{osSep}{Path.home()}{osSep}tmp')
        TestUmlShapesToXml.deleteDirectory(path=TestUmlShapesToXml.TEMPORARY_PATH)
        TestUmlShapesToXml.TEMPORARY_PATH.mkdir(exist_ok=True)

    def setUp(self):
        super().setUp()
        OGLInitialize()
        self._preferences: UmlPreferences = UmlPreferences()

    def tearDown(self):
        super().tearDown()

    def testEmptyProject(self):

        umlShapesToXml:     UmlShapesToXml = UmlShapesToXml(projectFileName=Path(''), projectCodePath=Path('/users/hasii'))
        actualEmptyProject: str            = umlShapesToXml.xml

        self.logger.debug(f'{actualEmptyProject=}')
        self.assertEqual(EXPECTED_EMPTY_PROJECT, actualEmptyProject, 'Empty project changed')

    def testEmptyDiagram(self):

        umlShapesToXml: UmlShapesToXml = UmlShapesToXml(projectFileName=Path(''), projectCodePath=Path('/users/hasii'))
        emptyDiagram:   UmlDocument     = UmlDocument()

        umlShapesToXml.serialize(umlDiagram=emptyDiagram)

        actualEmptyDiagram: str = umlShapesToXml.xml

        self.logger.debug(f'{actualEmptyDiagram=}')
        self.assertEqual(EXPECTED_EMPTY_DIAGRAM, actualEmptyDiagram, 'Empty diagram changed')

    def testSingleUmlClass(self):

        umlShapesToXml:     UmlShapesToXml = self._createXmlCreator()
        singleClassDiagram: UmlDocument     = self._createUmlDiagram(UmlDocumentType.CLASS_DOCUMENT, 'Unit Test Class Diagram')
        singleClass:        UmlClass       = self._createSingleClass()

        singleClass.id = 'play.small.long.group'        # So XML matches
        singleClass.pyutClass.id   = 0
        singleClass.pyutClass.name = 'ClassName1'

        singleClassDiagram.umlClasses.append(singleClass)
        umlShapesToXml.serialize(umlDiagram=singleClassDiagram)

        singleClassXML: str = umlShapesToXml.xml

        self.logger.debug(f'{singleClassXML=}')
        self._debugWriteToFile('SingleClass.xml', xml=singleClassXML)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SINGLE_CLASS_XML, singleClassXML, 'Class serialization changed')

    def testSingleUseCase(self):
        umlShapesToXml:       UmlShapesToXml = self._createXmlCreator()
        singleUseCaseDiagram: UmlDocument     = self._createUmlDiagram(UmlDocumentType.USE_CASE_DOCUMENT, 'Use Case Diagram')

        pyutUseCase: PyutUseCase = PyutUseCase(name='I am a lonely boy')
        pyutUseCase.id = 1
        umlUseCase:  UmlUseCase  = UmlUseCase(
            pyutUseCase=pyutUseCase,
            size=UmlDimensions(width=125, height=100)
        )
        umlUseCase.id = 'remember.central.issue.child'      # So XML matches

        umlUseCase.position = UmlPosition(x=300, y=500)

        singleUseCaseDiagram.umlUseCases.append(umlUseCase)
        umlShapesToXml.serialize(umlDiagram=singleUseCaseDiagram)

        singleUseCaseXML: str = umlShapesToXml.xml

        self.logger.debug(f'{singleUseCaseXML=}')
        self._debugWriteToFile('SingleUseCase.xml', xml=singleUseCaseXML)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SINGLE_USE_CASE_XML, singleUseCaseXML, 'Use Case serialization changed')

    def testSingleActor(self):
        umlShapesToXml:     UmlShapesToXml = self._createXmlCreator()
        singleActorDiagram: UmlDocument     = self._createUmlDiagram(UmlDocumentType.USE_CASE_DOCUMENT, 'Use Case Actor Diagram')

        pyutActor: PyutActor = PyutActor(actorName='LoboMalo')
        pyutActor.id = 0
        umlActor: UmlActor  = UmlActor(
            pyutActor=pyutActor,
            size=UmlDimensions(width=233, height=233)
        )
        umlActor.id       = 'remember.central.issue.child'
        umlActor.position = UmlPosition(x=500, y=200)

        singleActorDiagram.umlActors.append(umlActor)

        umlShapesToXml.serialize(singleActorDiagram)

        singleActorXML: str = umlShapesToXml.xml

        self.logger.debug(f'{singleActorXML=}')
        self._debugWriteToFile('SingleActor.xml', xml=singleActorXML)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SINGLE_ACTOR, singleActorXML, 'Actor serialization changed')

    def testSingleNote(self):

        umlShapesToXml:    UmlShapesToXml = self._createXmlCreator()
        singleNoteDiagram: UmlDocument     = self._createUmlDiagram(UmlDocumentType.USE_CASE_DOCUMENT, 'Uml Note Diagram')

        pyutNote: PyutNote = PyutNote(content='I am the best MAGA Note')
        pyutNote.id = 777

        umlNote: UmlNote = UmlNote(
            pyutNote=pyutNote,
            size=UmlDimensions(width=233, height=233)
        )
        umlNote.id       = 'remember.the.Alamo'
        umlNote.position = UmlPosition(x=666, y=777)

        singleNoteDiagram.umlNotes.append(umlNote)
        umlShapesToXml.serialize(umlDiagram=singleNoteDiagram)

        singleNoteXML: str = umlShapesToXml.xml

        self.logger.debug(f'{singleNoteXML=}')
        self._debugWriteToFile('SingleNote.xml', xml=singleNoteXML)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SINGLE_NOTE, singleNoteXML, 'Note serialization changed')

    def testSingleText(self):

        umlShapesToXml:    UmlShapesToXml = self._createXmlCreator()
        singleTextDiagram: UmlDocument     = self._createUmlDiagram(UmlDocumentType.CLASS_DOCUMENT, 'Uml Text Diagram')

        pyutText: PyutText = PyutText(content='Soy el mejor texto americano')
        pyutText.id = 1789

        umlText: UmlText = UmlText(
            pyutText=pyutText,
            size=UmlDimensions(width=150, height=50)
        )

        umlText.id       = 'remember.the.Alamo'
        umlText.position = UmlPosition(x=1024, y=768)

        singleTextDiagram.umlTexts.append(umlText)
        umlShapesToXml.serialize(umlDiagram=singleTextDiagram)

        singleTextXML: str = umlShapesToXml.xml

        self.logger.debug(f'{singleTextXML=}')
        self._debugWriteToFile('SingleText.xml', xml=singleTextXML)

        self.maxDiff = None
        self.assertEqual(EXPECTED_SINGLE_TEXT, singleTextXML, 'Note serialization changed')

    def testComplexClass(self):

        umlShapesToXml:       UmlShapesToXml = self._createXmlCreator()
        multipleClassDiagram: UmlDocument     = self._createUmlDiagram(UmlDocumentType.CLASS_DOCUMENT, 'Complex Class Diagram')

        classOne: UmlClass = self._createSingleClass(size=UmlDimensions(75, 75),   position=UmlPosition(333, 333))
        classTwo: UmlClass = self._createSingleClass(size=UmlDimensions(200, 100), position=UmlPosition(666, 666))

        classOne.pyutClass.addMethod(self._createSingleMethod())
        classOne.pyutClass.addMethod(self._createSingleMethod())

        classTwo.pyutClass.addMethod(self._createSingleMethod())
        classTwo.pyutClass.addMethod(self._createSingleMethod())

        classOne.pyutClass.addField(self._createSingleField())
        classOne.pyutClass.addField(self._createSingleField())

        classTwo.pyutClass.addField(self._createSingleField())
        classTwo.pyutClass.addField(self._createSingleField())

        displayParameterChoices: List[PyutDisplayParameters] = [
            PyutDisplayParameters.WITHOUT_PARAMETERS,
            PyutDisplayParameters.WITH_PARAMETERS,
            PyutDisplayParameters.UNSPECIFIED
        ]
        classOne.pyutClass.displayParameters = choice(displayParameterChoices)
        classTwo.pyutClass.displayParameters = choice(displayParameterChoices)
        self.logger.debug(f'{classOne.pyutClass.displayParameters=}')
        self.logger.debug(f'{classTwo.pyutClass.displayParameters=}')

        multipleClassDiagram.umlClasses.append(classOne)
        multipleClassDiagram.umlClasses.append(classTwo)

        umlShapesToXml.serialize(umlDiagram=multipleClassDiagram)

        multipleClassXML: str = umlShapesToXml.xml

        self.logger.debug(f'{multipleClassXML=}')

        self._debugWriteToFile('MultipleClassXML.xml', xml=multipleClassXML)

    def _createSingleClass(self, size: UmlDimensions = UmlDimensions(width=125, height=100), position: UmlPosition = UmlPosition(x=300, y=500)) -> UmlClass:
        """

        Args:
            size:
            position:

        Returns:
        """

        umlClass: UmlClass = UmlClass(
            pyutClass=self._createPyutClass(),
            size=size
        )

        umlClass.position = position
        return umlClass

    def _createPyutClass(self) -> PyutClass:

        className: str = f'{self._preferences.defaultClassName}{TestUmlShapesToXml.classCounter}'
        TestUmlShapesToXml.classCounter += 1

        pyutClass: PyutClass  = PyutClass(name=className)
        pyutClass.stereotype  = PyutStereotype.METACLASS
        pyutClass.showFields  = True
        pyutClass.showMethods = True
        pyutClass.displayParameters = PyutDisplayParameters.UNSPECIFIED

        return pyutClass

    def _createSingleMethod(self) -> PyutMethod:

        methodName: str = f'{self._preferences.defaultNameMethod}-{TestUmlShapesToXml.methodCounter}'
        TestUmlShapesToXml.methodCounter += 1
        pyutMethod: PyutMethod = PyutMethod(name=methodName)

        pyutParameter: PyutParameter = self._createSingleParameter()
        pyutMethod.addParameter(pyutParameter)

        return pyutMethod

    def _createSingleField(self) -> PyutField:

        fieldName: str = f'{self._preferences.defaultNameField}-{TestUmlShapesToXml.fieldCounter}'
        TestUmlShapesToXml.fieldCounter += 1

        pyutField:  PyutField            = PyutField(name=fieldName)
        visibility: List[PyutVisibility] = [PyutVisibility.PRIVATE, PyutVisibility.PROTECTED, PyutVisibility.PUBLIC]

        pyutField.visibility = choice(visibility)

        return pyutField

    def _createSingleParameter(self) -> PyutParameter:

        parameterName: str = f'{self._preferences.defaultNameParameter}-{TestUmlShapesToXml.parameterCounter}'
        TestUmlShapesToXml.parameterCounter += 1

        pyutParameter: PyutParameter  = PyutParameter(name=parameterName)
        typeList:      List[PyutType] = [PyutType(value='str'), PyutType(value='float'), PyutType(value='int')]

        pyutParameter.type = choice(typeList)
        self.logger.debug(f'{pyutParameter.type=}')

        return pyutParameter

    def _createXmlCreator(self) -> UmlShapesToXml:

        umlShapesToXml: UmlShapesToXml = UmlShapesToXml(projectFileName=Path(''), projectCodePath=Path('/users/hasii'))
        return umlShapesToXml

    def _debugWriteToFile(self, fileName: str, xml: str):

        p: Path = Path(f'/{TestUmlShapesToXml.TEMPORARY_PATH}/{fileName}')
        # p: Path = Path(f'/tmp/{fileName}')

        p.write_text(xml)

    @classmethod
    def deleteDirectory(cls, path: Path):
        """
        Will delete any files in the directory or subdirectories

        Args:
            path: The directory to delete

        """
        for posixPath in path.iterdir():
            if posixPath.is_dir():
                cls.deleteDirectory(posixPath)
            else:
                posixPath.unlink()
        path.rmdir()  # Remove the directory itself


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUmlShapesToXml))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
