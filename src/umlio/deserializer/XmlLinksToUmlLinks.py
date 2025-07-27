from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodelv2.PyutLink import LinkDestination
from pyutmodelv2.PyutLink import LinkSource
from umlshapes.types.Common import EndPoints
from untangle import Element

from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from umlshapes.links.UmlInheritance import UmlInheritance
from umlshapes.links.UmlLink import UmlLink

from umlshapes.shapes.UmlClass import UmlClass
from umlshapes.shapes.UmlNote import UmlNote
from umlshapes.shapes.UmlText import UmlText
from umlshapes.shapes.UmlUseCase import UmlUseCase
from wx import Point

from umlio.IOTypes import Elements

from umlio.IOTypes import LinkableUmlShape
from umlio.IOTypes import LinkableUmlShapes
from umlio.IOTypes import UmlLinkAttributes
from umlio.IOTypes import UmlLinks
from umlio.IOTypes import umlLinksFactory

from umlio.XMLConstants import XmlConstants

from umlio.deserializer.XmlToPyut import XmlToPyut


class XmlLinksToUmlLinks:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._xmlToPyut: XmlToPyut = XmlToPyut()

    def deserialize(self, umlDiagramElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLinks:

        umlLinks:     UmlLinks = umlLinksFactory()
        linkElements: Elements = cast(Elements, umlDiagramElement.get_elements(XmlConstants.ELEMENT_UML_LINK))

        for linkElement in linkElements:
            self.logger.info(f'{linkElement=}')
            self._umlLinkElementToUmlLink(umlLinkElement=linkElement, linkableUmlShapes=linkableUmlShapes)

        return umlLinks

    def _umlLinkElementToUmlLink(self, umlLinkElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLink | None:

        pyutLinkElements: Elements = cast(Elements, umlLinkElement.get_elements(XmlConstants.ELEMENT_MODEL_LINK))
        assert len(pyutLinkElements) == 1, 'There can only be one'

        singlePyutLinkElement: Element = pyutLinkElements[0]
        # <PyutLink name="" type="INHERITANCE" sourceId="111" destinationId="999" bidirectional="False" sourceCardinalityValue="" destinationCardinalityValue="" />
        sourceId: int = int(singlePyutLinkElement[XmlConstants.ATTRIBUTE_SOURCE_ID])
        dstId:    int = int(singlePyutLinkElement[XmlConstants.ATTRIBUTE_DESTINATION_ID])

        try:
            srcShape: LinkableUmlShape = linkableUmlShapes[sourceId]
            dstShape: LinkableUmlShape = linkableUmlShapes[dstId]
        except KeyError as ke:
            self.logger.error(f'{linkableUmlShapes=}')
            self.logger.error(f'Developer Error -- {singlePyutLinkElement=}')
            self.logger.error(f'Developer Error -- {sourceId=} {dstId=}  KeyError index: {ke}')
            return cast(UmlLink, None)

        # noinspection PyUnresolvedReferences
        pyutLink: PyutLink = self._xmlToPyut.linkToPyutLink(
            singleLink=singlePyutLinkElement,
            source=self._getSourceModelClass(srcShape),
            destination=self._getDestinationModelClass(dstShape)
        )
        self.logger.info(f'{pyutLink=}')
        umlLink: UmlLink = self._umlLinkFactory(srcShape=srcShape,
                                                pyutLink=pyutLink,
                                                destShape=dstShape,
                                                )

        umlLinkAttributes: UmlLinkAttributes = UmlLinkAttributes.fromGraphicLink(linkElement=umlLinkElement)
        self.logger.info(f'{umlLinkAttributes}=')

        umlLink.id        = umlLinkAttributes.id
        umlLink.spline    = umlLinkAttributes.spline
        # umlLink.InsertLineControlPoint()
        # umlLink.InsertLineControlPoint()
        umlLink.MakeLineControlPoints(n=2)       # Make this configurable

        umlLink.endPoints = EndPoints(
            toPosition=umlLinkAttributes.toPosition,
            fromPosition=umlLinkAttributes.fromPosition
        )

        return umlLink

    def _getSourceModelClass(self, linkableUmlShape: LinkableUmlShape) -> LinkSource:
        """

        Args:
            linkableUmlShape:

        Returns:  The appropriate model class instance
        """

        if isinstance(linkableUmlShape, UmlClass):
            return linkableUmlShape.pyutClass
        elif isinstance(linkableUmlShape, UmlNote):
            return linkableUmlShape.pyutNote
        elif isinstance(linkableUmlShape, UmlText):
            return linkableUmlShape.pyutText
        else:
            assert False, f'{linkableUmlShape=} is not a source linkable UML Shape'

    def _getDestinationModelClass(self, linkableUmlShape: LinkableUmlShape) -> LinkDestination:
        """

        Args:
            linkableUmlShape:

        Returns: The appropriate model class instance
        """

        if isinstance(linkableUmlShape, UmlClass):
            return linkableUmlShape.pyutClass
        elif isinstance(LinkableUmlShape, UmlUseCase):
            return linkableUmlShape.pyutUseCase
        else:
            assert False, f'{linkableUmlShape=} is not a destination linkable UML Shape'

    def _getLineControlPoints(self, umlLinkElement: Element) -> List[Point]:

        controlPoints: List[Point] = []

        return controlPoints

    def _umlLinkFactory(self, srcShape, pyutLink: PyutLink, destShape) -> UmlLink:

        if pyutLink.linkType == PyutLinkType.INHERITANCE:
            return UmlInheritance(baseClass=srcShape, pyutLink=pyutLink, subClass=destShape)
        else:
            assert False, f'Unknown link type, {pyutLink.linkType=}'
