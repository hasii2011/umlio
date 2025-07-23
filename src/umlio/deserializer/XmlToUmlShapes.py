
from logging import Logger
from logging import getLogger

from pathlib import Path

from untangle import Element
from untangle import parse

from codeallybasic.SecureConversions import SecureConversions

from umlio.IOTypes import UmlActors
from umlio.IOTypes import UmlClasses
from umlio.IOTypes import UmlDocument
from umlio.IOTypes import UmlDocumentTitle
from umlio.IOTypes import UmlDocumentType
from umlio.IOTypes import UmlNotes
from umlio.IOTypes import UmlTexts
from umlio.IOTypes import UmlProject
from umlio.IOTypes import UmlUseCases

from umlio.deserializer.XmlActorsToUmlActors import XmlActorsToUmlActors
from umlio.deserializer.XmlClassesToUmlClasses import XmlClassesToUmlClasses
from umlio.deserializer.XmlNotesToUmlNotes import XmlNotesToUmlNotes
from umlio.deserializer.XmlTextsToUmlTexts import XmlTextsToUmlTexts

from umlio.XMLConstants import XmlConstants
from umlio.deserializer.XmlUseCasesToUmlUseCases import XmlUseCasesToUmlUseCases


class XmlToUmlShapes:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._umlProject:  UmlProject  = UmlProject()

    @property
    def umlProject(self) -> UmlProject:
        return self._umlProject

    def deserializeProjectFile(self, fileName: Path):
        pass

    def deserializeXmlFile(self, fileName: Path):
        """
        Untangle the input Xml string to UmlShapes
        Args:
            fileName:  The file name from which the XML came from
        """

        xmlString: str = fileName.read_text()

        root:       Element = parse(xmlString)
        umlProject: Element = root.UmlProject

        self._umlProject.fileName = fileName
        self._umlProject.version  = umlProject[XmlConstants.ATTRIBUTE_VERSION]
        self._umlProject.codePath = umlProject[XmlConstants.ATTRIBUTE_CODE_PATH]

        for umlDiagramElement in umlProject.UMLDiagram:

            umlDiagram: UmlDocument = UmlDocument(
                documentTitle=umlDiagramElement[XmlConstants.ATTRIBUTE_TITLE],
                scrollPositionX=SecureConversions.secureInteger(umlDiagramElement[XmlConstants.ATTRIBUTE_SCROLL_POSITION_X]),
                scrollPositionY=SecureConversions.secureInteger(umlDiagramElement[XmlConstants.ATTRIBUTE_SCROLL_POSITION_Y]),
                pixelsPerUnitX=SecureConversions.secureInteger(umlDiagramElement[XmlConstants.ATTRIBUTE_PIXELS_PER_UNIT_X]),
                pixelsPerUnitY=SecureConversions.secureInteger(umlDiagramElement[XmlConstants.ATTRIBUTE_PIXELS_PER_UNIT_Y])
            )
            umlDiagram.documentTitle = UmlDocumentTitle(umlDiagramElement[XmlConstants.ATTRIBUTE_TITLE])

            if umlDiagramElement[XmlConstants.ATTRIBUTE_DOCUMENT_TYPE] == UmlDocumentType.CLASS_DOCUMENT.value:
                umlDiagram.documentType = UmlDocumentType.CLASS_DOCUMENT
                # document.oglClasses = self._graphicClassesToOglClasses(pyutDocument=pyutDocument)
                umlDiagram.umlClasses = self._deserializeUmlClassElements(umlDiagramElement=umlDiagramElement)
                umlDiagram.umlNotes   = self._deserializeUmlNoteElements(umlDiagramElement=umlDiagramElement)
                umlDiagram.umlTexts   = self._deserializeUmlTextElements(umlDiagramElement=umlDiagramElement)
            elif umlDiagramElement[XmlConstants.ATTRIBUTE_DOCUMENT_TYPE] == UmlDocumentType.USE_CASE_DOCUMENT.value:
                umlDiagram.documentType = UmlDocumentType.USE_CASE_DOCUMENT
                umlDiagram.umlNotes    = self._deserializeUmlNoteElements(umlDiagramElement=umlDiagramElement)
                umlDiagram.umlActors   = self._deserializeUmlActorElements(umlDiagramElement=umlDiagramElement)
                umlDiagram.umlUseCases = self._deserializeUmlUseCaseElements(umlDiagramElement=umlDiagramElement)
            else:
                umlDiagram.documentType = UmlDocumentType.SEQUENCE_DOCUMENT

            self._umlProject.umlDiagrams[umlDiagram.documentTitle] = umlDiagram

    def deserializeXml(self, rawXml: str):
        pass

    def _deserializeUmlClassElements(self, umlDiagramElement: Element) -> UmlClasses:

        umlClassesDeSerializer: XmlClassesToUmlClasses = XmlClassesToUmlClasses()
        umlClasses:            UmlClasses              = umlClassesDeSerializer.deserialize(umlDiagramElement=umlDiagramElement)

        return umlClasses

    def _deserializeUmlTextElements(self, umlDiagramElement: Element) -> UmlTexts:
        """
        Yeah, yeah, I know bad English;

        Args:
            umlDiagramElement:  The diagram Element

        Returns:  deserialized UmlText objects if any exist, else an empty list
        """
        umlTextDeSerializer: XmlTextsToUmlTexts = XmlTextsToUmlTexts()
        umlTexts: UmlTexts = umlTextDeSerializer.deserialize(umlDiagramElement=umlDiagramElement)

        return umlTexts

    def _deserializeUmlNoteElements(self, umlDiagramElement: Element) -> UmlNotes:
        """

        Args:
            umlDiagramElement:  The diagram Element

        Returns:  deserialized UmlNote objects if any exist, else an empty list
        """
        xmlNotesToUmlNotes: XmlNotesToUmlNotes = XmlNotesToUmlNotes()
        umlNotes: UmlNotes = xmlNotesToUmlNotes.deserialize(umlDiagramElement=umlDiagramElement)

        return umlNotes

    def _deserializeUmlActorElements(self, umlDiagramElement: Element) -> UmlActors:
        """

        Args:
            umlDiagramElement:  The diagram Element

        Returns:  deserialized UmlActor objects if any exist, else an empty list
        """
        xmlActorsToUmlActors: XmlActorsToUmlActors = XmlActorsToUmlActors()

        umlActors: UmlActors = xmlActorsToUmlActors.deserialize(umlDiagramElement=umlDiagramElement)

        return umlActors

    def _deserializeUmlUseCaseElements(self, umlDiagramElement: Element) -> UmlUseCases:
        """

        Args:
            umlDiagramElement:  The diagram Element

        Returns:  deserialized UmlUseCase objects if any exist, else an empty list
        """
        xmlUseCasesToUmlUseCases: XmlUseCasesToUmlUseCases = XmlUseCasesToUmlUseCases()

        umlUseCases: UmlUseCases = xmlUseCasesToUmlUseCases.deserialize(umlDiagramElement=umlDiagramElement)

        return umlUseCases
