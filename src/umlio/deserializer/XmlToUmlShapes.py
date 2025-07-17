
from logging import Logger
from logging import getLogger

from pathlib import Path

from untangle import Element
from untangle import parse

from codeallybasic.SecureConversions import SecureConversions

from umlio.IOTypes import UmlDiagram
from umlio.IOTypes import UmlDiagramTitle
from umlio.IOTypes import UmlDiagramType
from umlio.IOTypes import UmlTexts
from umlio.deserializer.XmlTextsToUmlTexts import XmlTextsToUmlTexts
from umlio.XMLConstants import XmlConstants

from umlio.IOTypes import UmlProject


class XmlToUmlShapes:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._umlProject:  UmlProject  = UmlProject()

    @property
    def umlProject(self) -> UmlProject:
        return self._umlProject

    def untangleProjectFile(self, fileName: Path):
        pass

    def untangleXmlFile(self, fileName: Path):
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
            umlDiagram.diagramTitle = UmlDiagramTitle(umlDiagramElement[XmlConstants.ATTRIBUTE_TITLE])

            if umlDiagramElement[XmlConstants.ATTRIBUTE_DIAGRAM_TYPE] == UmlDiagramType.CLASS_DIAGRAM.value:
                umlDiagram.diagramType = UmlDiagramType.CLASS_DIAGRAM
                # document.oglClasses = self._graphicClassesToOglClasses(pyutDocument=pyutDocument)
                # document.oglNotes   = self._graphicNotesToOglNotes(pyutDocument=pyutDocument)
                umlDiagram.umlTexts   = self._deserializeUmlTextElements(umlDiagramElement=umlDiagramElement)

            self._umlProject.umlDiagrams[umlDiagram.diagramTitle] = umlDiagram

    def untangleXml(self, rawXml: str):
        pass

    def _deserializeUmlTextElements(self, umlDiagramElement: Element) -> UmlTexts:
        """
        Yeah, yeah, I know bad English;

        Args:
            umlDiagramElement:  The Element document

        Returns:  untangled OglText objects if any exist, else an empty list
        """

        umlTextDeSerializer: XmlTextsToUmlTexts = XmlTextsToUmlTexts()
        umlTexts: UmlTexts = umlTextDeSerializer.deserialize(umlDiagramElement=umlDiagramElement)

        return umlTexts
