
from logging import Logger
from logging import getLogger

from pathlib import Path

from untangle import Element
from untangle import parse

from codeallybasic.SecureConversions import SecureConversions

from umlio.IOTypes import UmlDiagram
from umlio.IOTypes import UmlDiagramType
from umlio.SerializerV12.XMLConstants import XmlConstants

from umlio.IOTypes import UmlDiagrams
from umlio.IOTypes import UmlProject


class UnTangler:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._umlProject:  UmlProject  = UmlProject()
        self._umlDiagrams: UmlDiagrams = UmlDiagrams({})

    @property
    def umlProject(self) -> UmlProject:
        return self._umlProject

    @property
    def umlDiagrams(self) -> UmlDiagrams:
        return self.umlDiagrams

    def untangleFile(self, fileName: Path):
        pass

    def untangleXml(self, fileName: Path):
        """
        Untangle the input Xml string to UmlShapes
        Args:
            fileName:  The file name from which the XML came from
        """

        xmlString: str = fileName.read_text()

        root:       Element = parse(xmlString)
        umlProject: Element = root.UmlProject

        self._umlProject.version  = umlProject[XmlConstants.ATTRIBUTE_VERSION]
        self._umlProject.codePath = umlProject[XmlConstants.ATTRIBUTE_CODE_PATH]

        for umlDiagramElement in umlProject.UMLDiagram:

            umlDiagram: UmlDiagram = UmlDiagram(
                diagramTitle=umlDiagramElement[XmlConstants.ATTRIBUTE_TITLE],
                scrollPositionX=SecureConversions.secureInteger(umlDiagramElement[XmlConstants.ATTRIBUTE_SCROLL_POSITION_X]),
                scrollPositionY=SecureConversions.secureInteger(umlDiagramElement[XmlConstants.ATTRIBUTE_SCROLL_POSITION_Y]),
                pixelsPerUnitX=SecureConversions.secureInteger(umlDiagramElement[XmlConstants.ATTRIBUTE_PIXELS_PER_UNIT_X]),
                pixelsPerUnitY=SecureConversions.secureInteger(umlDiagramElement[XmlConstants.ATTRIBUTE_PIXELS_PER_UNIT_Y])
            )
            if umlDiagramElement[XmlConstants.ATTRIBUTE_DIAGRAM_TYPE] == UmlDiagramType.CLASS_DIAGRAM.value:
                umlDiagram.diagramType = UmlDiagramType.CLASS_DIAGRAM
                # document.oglClasses = self._graphicClassesToOglClasses(pyutDocument=pyutDocument)
                # document.oglNotes   = self._graphicNotesToOglNotes(pyutDocument=pyutDocument)
                # document.oglTexts   = self._graphicalTextToOglTexts(pyutDocument=pyutDocument)


    # def _extractProjectInformationForFile(self, fileName: Path):
    #     """
    #     Allows callers to inspect the project information.  For example the XML version
    #
    #     Args:
    #         fileName: The fully qualified file for a .xml or .put file
    #
    #     Returns:  A project information data class`
    #     """
    #     suffix: str = fileName.suffix
    #
    #     if suffix.endswith('.put') is False and suffix.endswith('.xml') is False:
    #         raise UnsupportedFileTypeException(message='File must end with .xml or .put extension')
    #
    #     if suffix.endswith('.xml'):
    #     elif suffix.endswith('.put'):
    #         xmlString = self.decompressFile(fqFileName=fileName)
    #     else:
    #         assert False, 'Unknown file suffix;  Should not get here'
    #
    #     root:        Element = parse(xmlString)
    #     pyutProject: Element = root.PyutProject
    #
    #     projectInformation = self._populateProjectInformation()
    #     projectInformation.fileName = fileName
    #
    #     return projectInformation

    def _populateProjectInformation(self, pyutProject: Element):

        self._umlProject.version  = pyutProject['version']
        self._umlProject.codePath = pyutProject['CodePath']
