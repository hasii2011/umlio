
from typing import Dict
from typing import List
from typing import Tuple
from typing import cast
from typing import Union
from typing import NewType

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from umlshapes.links.LabelType import LabelType
from umlshapes.links.UmlLinkLabel import UmlLinkLabel
from umlshapes.types.DeltaXY import DeltaXY
from umlshapes.types.UmlDimensions import UmlDimensions
from untangle import Element

from codeallybasic.SecureConversions import SecureConversions

from umlmodel.Link import Link
from umlmodel.Link import LinkDestination
from umlmodel.Link import LinkSource

from umlmodel.enumerations.LinkType import LinkType

from umlshapes.utils.BasicUtils import BasicUtils

from umlshapes.types.Common import EndPositions
from umlshapes.types.UmlPosition import UmlPosition
from umlshapes.types.UmlPosition import UmlPositions

from umlshapes.links.UmlLink import UmlLink
from umlshapes.links.UmlNoteLink import UmlNoteLink
from umlshapes.links.UmlAssociation import UmlAssociation
from umlshapes.links.UmlInheritance import UmlInheritance
from umlshapes.links.UmlComposition import UmlComposition
from umlshapes.links.UmlAggregation import UmlAggregation
from umlshapes.links.UmlInterface import UmlInterface

from umlshapes.shapes.UmlClass import UmlClass
from umlshapes.shapes.UmlNote import UmlNote
from umlshapes.shapes.UmlUseCase import UmlUseCase
from umlshapes.shapes.UmlActor import UmlActor

from umlshapes.ShapeTypes import UmlLinkGenre
from umlshapes.ShapeTypes import LinkableUmlShape
from umlshapes.ShapeTypes import LinkableUmlShapes


from umlio.IOTypes import Elements
from umlio.IOTypes import UmlLinkAttributes
from umlio.IOTypes import UmlLinks
from umlio.IOTypes import umlLinksFactory

from umlio.XMLConstants import XmlConstants
from umlio.deserializer.InvalidProjectXml import InvalidProjectXml

from umlio.deserializer.XmlToUmlModel import XmlToUmlModel


@dataclass
class ConnectedShapes:
    sourceShape:        LinkableUmlShape
    destinationShape:   LinkableUmlShape


UmlAssociationClasses = Union[UmlAssociation, UmlComposition, UmlAggregation]

# AssociationClassDescriptor = type[UmlAssociationClasses] = cast(type[LinkEventHandler], None)

LinkTypeToClass = NewType('LinkTypeToClass', Dict[LinkType, type[UmlAssociationClasses]])

CLASSMAP: LinkTypeToClass = LinkTypeToClass(
    {
        LinkType.ASSOCIATION: UmlAssociation,
        LinkType.AGGREGATION: UmlAggregation,
        LinkType.COMPOSITION: UmlComposition
    }
)
ASSOCIATION_LINK_TYPES: List[LinkType] = [
    LinkType.COMPOSITION, LinkType.AGGREGATION, LinkType.ASSOCIATION
]

DEFAULT_MISSING_LINK_LABEL_WIDTH:  int = 140
DEFAULT_MISSING_LINK_LABEL_HEIGHT: int = 24


class XmlLinksToUmlLinks:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._xmlToUmlModel: XmlToUmlModel = XmlToUmlModel()

    def deserialize(self, umlDiagramElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLinks:

        umlLinks:     UmlLinks = umlLinksFactory()
        linkElements: Elements = umlDiagramElement.get_elements(XmlConstants.ELEMENT_UML_LINK)

        for linkElement in linkElements:
            self.logger.debug(f'{linkElement=}')
            umlLink: UmlLink = self._umlLinkElementToUmlLink(umlLinkElement=linkElement, linkableUmlShapes=linkableUmlShapes)

            umlLinks.append(umlLink)

        return umlLinks

    def _umlLinkElementToUmlLink(self, umlLinkElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLink:

        linkElements: Elements = umlLinkElement.get_elements(XmlConstants.ELEMENT_MODEL_LINK)
        assert len(linkElements) == 1, 'There can only be one'      # noqa

        singleLinkElement: Element = linkElements[0]        # I hate this short cut

        umlLink: UmlLink = self._getUmlLink(umlLinkElement=umlLinkElement,
                                            singleLinkElement=singleLinkElement,
                                            linkableUmlShapes=linkableUmlShapes
                                            )

        BasicUtils.rationalizeTheLinkDataModel(umlLink=umlLink)

        return umlLink

    def _getUmlLink(self, umlLinkElement: Element, singleLinkElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLink:

        connectedShapes: ConnectedShapes = self._getConnectedShapes(singleLinkElement, linkableUmlShapes)
        link:            Link            = self._getLink(singleLinkElement, connectedShapes)

        umlLink: UmlLink = self._umlLinkFactory(srcShape=connectedShapes.sourceShape,
                                                link=link,
                                                destShape=connectedShapes.destinationShape,
                                                )
        if link.linkType in ASSOCIATION_LINK_TYPES:

            umlAssociation: UmlAssociation = cast(UmlAssociation, umlLink)
            umlAssociation.associationName        = self._getAssociationNameLabel(umlLinkElement, associationName=link.name)
            umlAssociation.sourceCardinality      = self._getSourceCardinalityNameLabel(umlLinkElement, sourceCardinality=link.sourceCardinality)
            umlAssociation.destinationCardinality = self._getDestinationCardinalityNameLabel(umlLinkElement, destinationCardinality=link.destinationCardinality)

        umlLinkAttributes: UmlLinkAttributes = UmlLinkAttributes.fromGraphicLink(linkElement=umlLinkElement)
        self.logger.debug(f'{umlLinkAttributes}=')

        umlLink.id        = umlLinkAttributes.id
        umlLink.spline    = umlLinkAttributes.spline

        umlLink.MakeLineControlPoints(n=2)       # Make this configurable

        umlLink.endPositions = EndPositions(
            toPosition=umlLinkAttributes.toPosition,
            fromPosition=umlLinkAttributes.fromPosition
        )
        controlPoints: UmlPositions = self._getLineControlPoints(umlLinkElement=umlLinkElement)
        for cp in controlPoints:
            umlLink.addLineControlPoint(umlPosition=cp)

        return umlLink

    def _getLink(self, modelLinkElement: Element, connectedShapes: ConnectedShapes) -> Link:
        """

        Args:
            modelLinkElement:   The Xml Elements
            connectedShapes:    The shapes at the ends of the link

        Returns:    A data model link
        """

        # noinspection PyUnresolvedReferences
        link: Link = self._xmlToUmlModel.linkToModelLink(
            singleLink=modelLinkElement,
            source=self._getLinkSourceModelClass(connectedShapes.sourceShape),
            destination=self._getLinkDestinationModelClass(connectedShapes.destinationShape)
        )
        self.logger.debug(f'{link=}')

        return link

    def _getConnectedShapes(self, linkElement: Element, linkableUmlShapes: LinkableUmlShapes) -> ConnectedShapes:
        """

        Args:
            linkElement:
            linkableUmlShapes:   The dictionary of potential shapes

        Returns:  The connected shapes;  Will assert if it cannot find them
        """
        sourceId: str | None = linkElement[XmlConstants.ATTRIBUTE_SOURCE_ID]
        dstId:    str | None = linkElement[XmlConstants.ATTRIBUTE_DESTINATION_ID]

        if sourceId is None or dstId is None:
            raise InvalidProjectXml(f'Links must have source and destination IDs.  {sourceId=} {dstId=}')

        try:
            sourceShape:      LinkableUmlShape = linkableUmlShapes[sourceId]
            destinationShape: LinkableUmlShape = linkableUmlShapes[dstId]
        except KeyError as ke:
            self.logger.error(f'{linkableUmlShapes=}')
            self.logger.error(f'Developer Error -- {linkElement=}')     # noqa
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
            return linkableUmlShape.modelClass
        elif isinstance(linkableUmlShape, UmlNote):
            return linkableUmlShape.modelNote
        # elif isinstance(linkableUmlShape, UmlText):
        #     return linkableUmlShape.modelText
        elif isinstance(linkableUmlShape, UmlActor):
            return linkableUmlShape.modelActor
        else:
            assert False, f'{linkableUmlShape=} is not a source linkable UML Shape'

    def _getLinkDestinationModelClass(self, linkableUmlShape: LinkableUmlShape) -> LinkDestination:
        """

        Args:
            linkableUmlShape:

        Returns: The appropriate model class instance
        """

        if isinstance(linkableUmlShape, UmlClass):
            return linkableUmlShape.modelClass
        elif isinstance(linkableUmlShape, UmlUseCase):
            return linkableUmlShape.modelUseCase
        else:
            assert False, f'{linkableUmlShape=} is not a destination linkable UML Shape'

    def _getLineControlPoints(self, umlLinkElement: Element) -> UmlPositions:
        """
         <LineControlPoint x="100" y="100" />

        Args:
            umlLinkElement:

        Returns:
        """

        controlPoints: UmlPositions = UmlPositions([])

        controlPointElements: Elements = umlLinkElement.get_elements(XmlConstants.ELEMENT_MODEL_LINE_CONTROL_POINT)
        for controlPointElement in controlPointElements:
            x: int = SecureConversions.secureInteger(cast(str, controlPointElement[XmlConstants.ATTRIBUTE_X]))
            y: int = SecureConversions.secureInteger(cast(str, controlPointElement[XmlConstants.ATTRIBUTE_Y]))

            umlPosition: UmlPosition = UmlPosition(x=x, y=y)
            controlPoints.append(umlPosition)

        return controlPoints

    def _umlLinkFactory(self, srcShape: LinkableUmlShape, link: Link, destShape: LinkableUmlShape) -> UmlLinkGenre:
        """

        Args:
            srcShape:
            link:
            destShape:

        Returns:  The appropriate UML Link shape
        """
        if link.linkType == LinkType.INHERITANCE:
            # Note dest and source are reversed here
            subClass:  UmlClass = srcShape              # type: ignore
            baseClass: UmlClass = destShape             # type: ignore

            umlInheritance: UmlInheritance = UmlInheritance(baseClass=baseClass, link=link, subClass=subClass)

            return umlInheritance

        elif link.linkType in ASSOCIATION_LINK_TYPES:
            umlAssociation = CLASSMAP[link.linkType](link)
            #
            # Need to do this because the shape is not yet on a canvas
            #
            umlAssociation.sourceShape      = srcShape
            umlAssociation.destinationShape = destShape
            return umlAssociation
        elif link.linkType == LinkType.NOTELINK:
            umlNote:     UmlNote     = srcShape         # type: ignore
            umlClass:    UmlClass    = destShape        # type: ignore
            umlNoteLink: UmlNoteLink = UmlNoteLink(link=link)
            umlNoteLink.sourceNote       = umlNote
            umlNoteLink.destinationClass = umlClass
            return umlNoteLink
        elif link.linkType == LinkType.INTERFACE:
            implementingClass: UmlClass = srcShape      # type: ignore
            interfaceClass:    UmlClass = destShape     # type: ignore
            umlInterface: UmlInterface = UmlInterface(link=link, implementingClass=implementingClass, interfaceClass=interfaceClass)

            return umlInterface
        else:
            assert False, f'Unknown link type, {link.linkType=}'

    def _getAssociationNameLabel(self, umlLinkElement: Element, associationName: str) -> UmlLinkLabel:
        """
            <AssociationName width="75" height="24" deltaX="0" deltaY="0" />

        Args:
            umlLinkElement: The <UmlLink> XML element containing the <AssociationName> child tag
            associationName: The association name

        Returns:  A deserialized link label that represents the association name
        """
        nameElement: Element = umlLinkElement.AssociationName

        umlLinkLabel: UmlLinkLabel = self._getNameLabel(labelElement=nameElement, text=associationName, labelType=LabelType.ASSOCIATION_NAME)
        return umlLinkLabel

    def _getSourceCardinalityNameLabel(self, umlLinkElement: Element, sourceCardinality: str) -> UmlLinkLabel:
        """
        <SourceCardinality width="100" height="24" deltaX="0" deltaY="0" />

        Args:
            umlLinkElement:     The <UmlLink> XML element containing the <SourceCardinality> child tag
            sourceCardinality:  The value of the source cardinality

        Returns:  A deserialized link label that represents the link source cardinality

        """
        nameElement: Element = umlLinkElement.SourceCardinality
        umlLinkLabel: UmlLinkLabel = self._getNameLabel(labelElement=nameElement, text=sourceCardinality, labelType=LabelType.SOURCE_CARDINALITY)

        return umlLinkLabel

    def _getDestinationCardinalityNameLabel(self, umlLinkElement: Element, destinationCardinality: str) -> UmlLinkLabel:
        """
        <DestinationCardinality width="100" height="24" deltaX="0" deltaY="0" />

        Args:
            umlLinkElement:     The <UmlLink> XML element containing the <DestinationCardinality> child tag
            destinationCardinality:  The value of the destination cardinality

        Returns:  A deserialized link label that represents the link destination cardinality

        """

        nameElement: Element = umlLinkElement.DestinationCardinality
        umlLinkLabel: UmlLinkLabel = self._getNameLabel(labelElement=nameElement, text=destinationCardinality, labelType=LabelType.DESTINATION_CARDINALITY)

        return umlLinkLabel

    def _getNameLabel(self, labelElement: Element, text: str, labelType: LabelType) -> UmlLinkLabel:

        umlLinkLabel: UmlLinkLabel = UmlLinkLabel(label=text, labelType=labelType)

        self.logger.info(f'Get link name attributes for: {labelType.value}')

        size:      UmlDimensions
        linkDelta: DeltaXY
        size, linkDelta = self._getLinkNameAttributes(nameElement=labelElement)

        umlLinkLabel.size      = size
        umlLinkLabel.linkDelta = linkDelta

        return umlLinkLabel

    def _getLinkNameAttributes(self, nameElement: Element) -> Tuple[UmlDimensions, DeltaXY]:
        """
        Put in some temp code for old project that do not have the width/height attributes on UmlLinkLabel's
        Args:
            nameElement:  A general element for association name, source/destination cardinality,

        Returns: A tuple of the UmlDimensions and DeltaXY attributes of a UmlLinkLabel

        """
        widthStr: str | None  = nameElement[XmlConstants.ATTRIBUTE_WIDTH]
        width:    int
        if widthStr is None:
            width = DEFAULT_MISSING_LINK_LABEL_WIDTH
            self.logger.warning(f'Missing link label width, synthesized the value: {DEFAULT_MISSING_LINK_LABEL_WIDTH}')
        else:
            width = SecureConversions.secureInteger(widthStr)

        heightStr: str | None = nameElement[XmlConstants.ATTRIBUTE_HEIGHT]
        height:    int
        if heightStr is None:
            height = DEFAULT_MISSING_LINK_LABEL_HEIGHT
            self.logger.warning(f'Missing link label height, synthesized the value: {DEFAULT_MISSING_LINK_LABEL_HEIGHT}')
        else:
            height = SecureConversions.secureInteger(heightStr)

        deltaXStr: str = cast(str, nameElement[XmlConstants.ATTRIBUTE_DELTA_X])
        deltaYStr: str = cast(str, nameElement[XmlConstants.ATTRIBUTE_DELTA_Y])

        deltaX: int = SecureConversions.secureInteger(deltaXStr)
        deltaY: int = SecureConversions.secureInteger(deltaYStr)

        size: UmlDimensions = UmlDimensions(width=width, height=height)
        linkDelta: DeltaXY = DeltaXY(deltaX=deltaX, deltaY=deltaY)

        return size, linkDelta
