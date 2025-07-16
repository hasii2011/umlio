
from typing import cast

from logging import Logger
from logging import getLogger

from untangle import Element

from umlshapes.shapes.UmlText import UmlText

from pyutmodelv2.PyutText import PyutText

from umlio.IOTypes import Elements
from umlio.IOTypes import GraphicInformation
from umlio.IOTypes import UmlTexts
from umlio.IOTypes import umlTextsFactory
from umlio.deserializer.UnTanglePyut import UnTanglePyut
from umlio.serializer.XMLConstants import XmlConstants


class deserializeUmlTexts:
    """
    Yes, I know bad English
    """
    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._untanglePyut: UnTanglePyut = UnTanglePyut()

    def unTangle(self, umlDiagram: Element) -> UmlTexts:
        """

        Args:
            umlDiagram:  The Element document

        Returns:  untangled OglText objects if any exist, else an empty list
        """

        umlTexts:     UmlTexts = umlTextsFactory()
        textElements: Elements = cast(Elements, umlDiagram.get_elements(XmlConstants.ELEMENT_UML_TEXT))

        for graphicText in textElements:
            self.logger.debug(f'{graphicText}')

            graphicInformation: GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=graphicText)

            pyutText: PyutText = self._untanglePyut.textToPyutText(graphicText=graphicText)
            umlText:  UmlText  = UmlText(pyutText=pyutText, size=graphicInformation.size)

            umlText.position = graphicInformation.position
            umlText.pyutText = pyutText

            umlTexts.append(umlText)

        return umlTexts
