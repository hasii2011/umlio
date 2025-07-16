
from typing import cast

from logging import Logger
from logging import getLogger

from untangle import Element

from pyutmodelv2.PyutText import PyutText

from umlshapes.shapes.UmlText import UmlText

from umlio.IOTypes import Elements
from umlio.IOTypes import GraphicInformation
from umlio.IOTypes import UmlTexts
from umlio.IOTypes import umlTextsFactory

from umlio.deserializer.UnTanglePyut import UnTanglePyut

from umlio.serializer.XMLConstants import XmlConstants


class UmlTextDeSerializer:
    """
    Yes, I know bad English
    """
    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._untanglePyut: UnTanglePyut = UnTanglePyut()

    def deserialize(self, umlDiagramElement: Element) -> UmlTexts:
        """

        Args:
            umlDiagramElement:  The Element document

        Returns:  deserialized UmlText objects if any exist, else an empty list
        """

        umlTexts:     UmlTexts = umlTextsFactory()
        textElements: Elements = cast(Elements, umlDiagramElement.get_elements(XmlConstants.ELEMENT_UML_TEXT))

        for textElement in textElements:
            self.logger.debug(f'{textElement}')

            graphicInformation: GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=textElement)
            pyutText:           PyutText           = self._untanglePyut.textToPyutText(graphicText=textElement)
            umlText:            UmlText            = UmlText(pyutText=pyutText)

            umlText.id       = graphicInformation.id
            umlText.size     = graphicInformation.size
            umlText.position = graphicInformation.position

            umlText.pyutText = pyutText
            umlTexts.append(umlText)

        return umlTexts
