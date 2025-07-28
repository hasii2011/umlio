
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import Point

from untangle import Element

from codeallybasic.SecureConversions import SecureConversions

from pyutmodelv2.PyutLink import LinkDestination
from pyutmodelv2.PyutLink import LinkSource
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from umlshapes.types.Common import EndPoints

from umlshapes.links.UmlInheritance import UmlInheritance
from umlshapes.links.UmlLink import UmlLink

from umlshapes.shapes.UmlClass import UmlClass
from umlshapes.shapes.UmlNote import UmlNote
from umlshapes.shapes.UmlText import UmlText
from umlshapes.shapes.UmlUseCase import UmlUseCase

from umlio.IOTypes import Elements
from umlio.IOTypes import LinkableUmlShape
from umlio.IOTypes import LinkableUmlShapes
from umlio.IOTypes import UmlLinkAttributes
from umlio.IOTypes import UmlLinks
from umlio.IOTypes import umlLinksFactory

from umlio.XMLConstants import XmlConstants

from umlio.deserializer.XmlToPyut import XmlToPyut


@dataclass
class ConnectedShapes:
    sourceShape:        LinkableUmlShape
    destinationShape:   LinkableUmlShape


class XmlLinksToUmlLinks:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._xmlToPyut: XmlToPyut = XmlToPyut()

    def deserialize(self, umlDiagramElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLinks:

        umlLinks:     UmlLinks = umlLinksFactory()
        linkElements: Elements = cast(Elements, umlDiagramElement.get_elements(XmlConstants.ELEMENT_UML_LINK))

        for linkElement in linkElements:
            self.logger.info(f'{linkElement=}')
            umlLink: UmlLink = self._umlLinkElementToUmlLink(umlLinkElement=linkElement, linkableUmlShapes=linkableUmlShapes)

            umlLinks.append(umlLink)
        return umlLinks

    def _umlLinkElementToUmlLink(self, umlLinkElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLink:

        pyutLinkElements: Elements = cast(Elements, umlLinkElement.get_elements(XmlConstants.ELEMENT_MODEL_LINK))
        assert len(pyutLinkElements) == 1, 'There can only be one'

        singlePyutLinkElement: Element = pyutLinkElements[0]        # I hate this short cut

        umlLink: UmlLink = self._getUmlLink(umlLinkElement=umlLinkElement,
                                            singlePyutLinkElement=singlePyutLinkElement,
                                            linkableUmlShapes=linkableUmlShapes
                                            )

        return umlLink

    def _getUmlLink(self, umlLinkElement: Element, singlePyutLinkElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLink:

        connectedShapes: ConnectedShapes = self._getConnectedShapes(singlePyutLinkElement, linkableUmlShapes)
        pyutLink:        PyutLink        = self._getPyutLink(singlePyutLinkElement, connectedShapes)

        umlLink: UmlLink = self._umlLinkFactory(srcShape=connectedShapes.sourceShape,
                                                pyutLink=pyutLink,
                                                destShape=connectedShapes.destinationShape,
                                                )

        umlLinkAttributes: UmlLinkAttributes = UmlLinkAttributes.fromGraphicLink(linkElement=umlLinkElement)
        self.logger.info(f'{umlLinkAttributes}=')

        umlLink.id        = umlLinkAttributes.id
        umlLink.spline    = umlLinkAttributes.spline

        umlLink.MakeLineControlPoints(n=2)       # Make this configurable

        umlLink.endPoints = EndPoints(
            toPosition=umlLinkAttributes.toPosition,
            fromPosition=umlLinkAttributes.fromPosition
        )
        controlPoints: List[Point] = self._getLineControlPoints(umlLinkElement=umlLinkElement)
        for cp in controlPoints:
            umlLink.InsertLineControlPoint(point=cp)

        return umlLink

    def _getPyutLink(self, pyutLinkElement: Element, connectedShapes: ConnectedShapes) -> PyutLink:
        """

        Args:
            pyutLinkElement:    The Xml Elements
            connectedShapes:    The shapes at the ends of the link

        Returns:    A data model link
        """

        # noinspection PyUnresolvedReferences
        pyutLink: PyutLink = self._xmlToPyut.linkToPyutLink(
            singleLink=pyutLinkElement,
            source=self._getLinkSourceModelClass(connectedShapes.sourceShape),
            destination=self._getLinkDestinationModelClass(connectedShapes.destinationShape)
        )
        self.logger.info(f'{pyutLink=}')

        return pyutLink

    def _getConnectedShapes(self, pyutLinkElement: Element, linkableUmlShapes: LinkableUmlShapes) -> ConnectedShapes:
        """

        Args:
            pyutLinkElement:
            linkableUmlShapes:   The dictionary of potential shapes

        Returns:  The connected shapes;  Will assert if it cannot find them
        """
        sourceId: int = int(pyutLinkElement[XmlConstants.ATTRIBUTE_SOURCE_ID])
        dstId:    int = int(pyutLinkElement[XmlConstants.ATTRIBUTE_DESTINATION_ID])

        try:
            sourceShape:      LinkableUmlShape = linkableUmlShapes[sourceId]
            destinationShape: LinkableUmlShape = linkableUmlShapes[dstId]
        except KeyError as ke:
            self.logger.error(f'{linkableUmlShapes=}')
            self.logger.error(f'Developer Error -- {pyutLinkElement=}')
            self.logger.error(f'Developer Error -- {sourceId=} {dstId=}  KeyError index: {ke}')
            assert False, 'Developer error'

        return ConnectedShapes(sourceShape=sourceShape, destinationShape=destinationShape)

    def _getLinkSourceModelClass(self, linkableUmlShape: LinkableUmlShape) -> LinkSource:
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

    def _getLinkDestinationModelClass(self, linkableUmlShape: LinkableUmlShape) -> LinkDestination:
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
        """
         <LineControlPoint x="100" y="100" />

        Args:
            umlLinkElement:

        Returns:
        """

        controlPoints: List[Point] = []

        controlPointElements: Elements = cast(Elements, umlLinkElement.get_elements(XmlConstants.ELEMENT_MODEL_LINE_CONTROL_POINT))
        for controlPointElement in controlPointElements:
            x: int = SecureConversions.secureInteger(controlPointElement[XmlConstants.ATTRIBUTE_X])
            y: int = SecureConversions.secureInteger(controlPointElement[XmlConstants.ATTRIBUTE_Y])

            point: Point = Point(x=x, y=y)
            controlPoints.append(point)

        return controlPoints

    def _umlLinkFactory(self, srcShape, pyutLink: PyutLink, destShape) -> UmlLink:

        if pyutLink.linkType == PyutLinkType.INHERITANCE:
            # Note dest and source are reversed here
            return UmlInheritance(baseClass=destShape, pyutLink=pyutLink, subClass=srcShape)
        else:
            assert False, f'Unknown link type, {pyutLink.linkType=}'
