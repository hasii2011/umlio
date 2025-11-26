
from typing import Dict
from typing import NewType
from typing import cast
from typing import Tuple

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from umlmodel.Class import Class
from umlmodel.Interface import Interface
from umlmodel.Link import Link
from umlmodel.ModelTypes import ClassName
from umlmodel.Note import Note
from umlmodel.enumerations.LinkType import LinkType
from umlshapes.links.UmlLollipopInterface import UmlLollipopInterface
from umlshapes.links.UmlNoteLink import UmlNoteLink
from umlshapes.shapes.UmlNote import UmlNote
from umlshapes.types.Common import AttachmentSide

from wx import Point

from umlshapes.links.UmlInterface import UmlInterface
from umlshapes.links.UmlInheritance import UmlInheritance
from umlshapes.links.UmlAssociation import UmlAssociation
from umlshapes.links.UmlLink import UmlLink

from umlshapes.shapes.UmlClass import UmlClass

from umlshapes.frames.DiagramFrame import DiagramFrame

from umlshapes.types.UmlPosition import UmlPosition

BASE_UML_CLASS_NAME:     str = 'BaseClass'
SUBCLASS_UML_CLASS_NAME: str = 'SubClass'
BASE_UML_CLASS_ID:       str = 'call.lose.current.group'
SUBCLASS_UML_CLASS_ID:   str = 'speak.left.economic.change'
BASE_CLASS_PYUT_ID:      str = '999'
SUBCLASS_PYUT_ID:        str = '111'

SOURCE_PYUT_CLASS_ID:      str = '666'
DESTINATION_PYUT_CLASS_ID: str = '777'

SOURCE_UML_CLASS_ID:      str = 'provide.serious.hand.change'
DESTINATION_UML_CLASS_ID: str = 'believe.able.power.moment'

INTERFACE_UML_CLASS_NAME:    str = 'Interface'
IMPLEMENTING_UML_CLASS_NAME: str = 'Implementor'
INTERFACE_UML_CLASS_ID:      str = 'card.carrying.interface'
IMPLEMENTING_UML_CLASS_ID:   str = 'valley.darkness.implementor'
INTERFACE_PYUT_CLASS_ID:     str = '2222'
IMPLEMENTING_PYUT_CLASS_ID:  str = '4444'

UML_LINK_CANONICAL_MONIKER: str = 'die.free.open.point'

CANONICAl_LOLLIPOP_NAME:     str            = 'IFake'
LOLLIPOP_ATTACHMENT_SIDE:    AttachmentSide = AttachmentSide.RIGHT
PYUT_INTERFACE_CANONICAL_ID: str            = '0xDEADBEEF'

DESTINATION_UML_CLASS_NAME: str = 'DestinationClass'
PYUT_NOTE_ID:               str = '6262'


@dataclass
class LinkDescription:
    associationClass:   type[UmlAssociation]
    linkType:           LinkType = LinkType.ASSOCIATION
    associationCounter: int = 0
    classCounter:       int = 0


LinkDescriptions = NewType('LinkDescriptions', Dict[LinkType, LinkDescription])


@dataclass
class CreatedLink:
    sourceUmlClass:      UmlClass             = cast(UmlClass, None)
    association:         UmlLink              = cast(UmlLink, None)
    destinationUmlClass: UmlClass             = cast(UmlClass, None)


@dataclass
class CreatedNoteLink:
    sourceNote:          UmlNote     = cast(UmlNote, None)
    destinationUmlClass: UmlClass    = cast(UmlClass, None)
    umlNoteLink:         UmlNoteLink = cast(UmlNoteLink, None)


class LinkCreator:
    def __init__(self, diagramFrame: DiagramFrame):
        self.logger: Logger = getLogger(__name__)

        self._diagramFrame: DiagramFrame = diagramFrame

        association: LinkDescription = LinkDescription(
            linkType=LinkType.ASSOCIATION,
            associationClass=UmlAssociation
        )

        self._relationShips: LinkDescriptions = LinkDescriptions(
            {
                LinkType.ASSOCIATION: association,
                # Identifiers.ID_DISPLAY_UML_COMPOSITION: composition,
                # Identifiers.ID_DISPLAY_UML_AGGREGATION: aggregation,
            }
        )

    # noinspection PyTypeChecker
    def createAssociation(self, linkType: LinkType) -> CreatedLink:

        associationDescription: LinkDescription = self._relationShips[linkType]

        return self._createAssociation(associationDescription=associationDescription)

    def _createAssociation(self, associationDescription: LinkDescription) -> CreatedLink:
        """

        Args:
            associationDescription:
        """
        sourceUmlClass, destinationUmlClass = self._createClassPair(associationDescription.classCounter)
        associationDescription.classCounter += 2

        self.logger.info(f'{sourceUmlClass.id=} {destinationUmlClass.id=}')

        pyutLink = self._createAssociationPyutLink(pyutSource=sourceUmlClass.modelClass,
                                                   pyutDestination=destinationUmlClass.modelClass,
                                                   associationCounter=associationDescription.associationCounter
                                                   )

        associationDescription.associationCounter += 1

        umlAssociation = associationDescription.associationClass(pyutLink)

        umlAssociation.id = UML_LINK_CANONICAL_MONIKER
        umlAssociation.SetCanvas(self._diagramFrame)
        if pyutLink.linkType != LinkType.LOLLIPOP:
            umlAssociation.MakeLineControlPoints(n=2)

        sourceUmlClass.addLink(umlLink=umlAssociation, destinationClass=destinationUmlClass)

        return CreatedLink(
            sourceUmlClass=sourceUmlClass,
            destinationUmlClass=destinationUmlClass,
            association=umlAssociation
        )

    def createUmlInheritance(self) -> CreatedLink:

        basePyutClass: Class = Class(name=f'{BASE_UML_CLASS_NAME}')
        subPyutClass:  Class = Class(name=f'{SUBCLASS_UML_CLASS_NAME}')

        basePyutClass.id = BASE_CLASS_PYUT_ID
        subPyutClass.id  = SUBCLASS_PYUT_ID

        baseUmlClass:     UmlClass = UmlClass(modelClass=basePyutClass)
        subClassUmlClass: UmlClass = UmlClass(modelClass=subPyutClass)

        baseUmlClass.id       = BASE_UML_CLASS_ID
        subClassUmlClass.id   = SUBCLASS_UML_CLASS_ID

        baseUmlClass.position     = UmlPosition(x=100, y=100)
        subClassUmlClass.position = UmlPosition(x=200, y=300)

        baseUmlClass.SetCanvas(self._diagramFrame)
        subClassUmlClass.SetCanvas(self._diagramFrame)

        pyutInheritance: Link = Link(linkType=LinkType.INHERITANCE, source=subPyutClass, destination=basePyutClass)

        umlInheritance: UmlInheritance = UmlInheritance(link=pyutInheritance, baseClass=baseUmlClass, subClass=subClassUmlClass)

        umlInheritance.id = UML_LINK_CANONICAL_MONIKER

        umlInheritance.SetCanvas(self._diagramFrame)
        umlInheritance.MakeLineControlPoints(n=2)       # Make this configurable

        umlInheritance.SetEnds(x1=0, y1=0, x2=0, y2=0)
        umlInheritance.InsertLineControlPoint(point=Point(x=100, y=100))
        umlInheritance.InsertLineControlPoint(point=Point(x=200, y=200))

        # REMEMBER:   from subclass to base class
        subClassUmlClass.addLink(umlLink=umlInheritance, destinationClass=baseUmlClass)

        return CreatedLink(
            sourceUmlClass=subClassUmlClass,
            destinationUmlClass=baseUmlClass,
            association=umlInheritance
        )

    def createUmlInterface(self) -> CreatedLink:

        interfacePyutClass:    Class = Class(name=f'{INTERFACE_UML_CLASS_NAME}')
        implementingPyutClass: Class = Class(name=f'{IMPLEMENTING_UML_CLASS_NAME}')

        interfacePyutClass.id    = INTERFACE_PYUT_CLASS_ID
        implementingPyutClass.id = IMPLEMENTING_PYUT_CLASS_ID

        interfaceUmlClass:    UmlClass = UmlClass(modelClass=interfacePyutClass)
        implementingUmlClass: UmlClass = UmlClass(modelClass=implementingPyutClass)

        interfaceUmlClass.id    = INTERFACE_UML_CLASS_ID
        implementingUmlClass.id = IMPLEMENTING_UML_CLASS_ID

        interfaceUmlClass.position    = UmlPosition(x=3333, y=3333)
        implementingUmlClass.position = UmlPosition(x=4444, y=4444)

        interfaceUmlClass.SetCanvas(self._diagramFrame)
        implementingUmlClass.SetCanvas(self._diagramFrame)

        pyutInterface: Link = Link(linkType=LinkType.INTERFACE, source=implementingPyutClass, destination=interfacePyutClass)     # TODO use PyutInterface

        umlInterface: UmlInterface = UmlInterface(link=pyutInterface, interfaceClass=interfaceUmlClass, implementingClass=implementingUmlClass)

        umlInterface.id = UML_LINK_CANONICAL_MONIKER

        umlInterface.SetCanvas(self._diagramFrame)
        umlInterface.MakeLineControlPoints(n=2)       # Make this configurable

        umlInterface.InsertLineControlPoint(point=Point(x=372, y=433))
        umlInterface.InsertLineControlPoint(point=Point(x=400, y=433))

        # REMEMBER:   from subclass to base class
        implementingUmlClass.addLink(umlLink=umlInterface, destinationClass=interfaceUmlClass)

        return CreatedLink(
            sourceUmlClass=implementingUmlClass,
            destinationUmlClass=interfaceUmlClass,
            association=umlInterface
        )

    def createLollipop(self):

        # Need the model
        implementingPyutClass: Class = Class(name=f'{IMPLEMENTING_UML_CLASS_NAME}')
        implementingPyutClass.id = IMPLEMENTING_PYUT_CLASS_ID

        # Need the attached to UI Shape
        implementingUmlClass: UmlClass = UmlClass(modelClass=implementingPyutClass)
        implementingUmlClass.id       = IMPLEMENTING_UML_CLASS_ID
        implementingUmlClass.position = UmlPosition(x=3333, y=3333)

        # fill out the model
        pyutInterface: Interface = Interface(name=CANONICAl_LOLLIPOP_NAME)
        pyutInterface.id = PYUT_INTERFACE_CANONICAL_ID
        pyutInterface.addImplementor(ClassName(implementingPyutClass.name))

        # Need the lollipop
        umlLollipopInterface: UmlLollipopInterface = UmlLollipopInterface(interface=pyutInterface)
        umlLollipopInterface.attachedTo     = implementingUmlClass
        umlLollipopInterface.attachmentSide = LOLLIPOP_ATTACHMENT_SIDE

        return umlLollipopInterface, implementingUmlClass

    def createNoteLink(self) -> CreatedNoteLink:

        # Need the model
        destinationPyutClass: Class = Class(name=f'{DESTINATION_UML_CLASS_NAME}')
        destinationPyutClass.id = DESTINATION_PYUT_CLASS_ID

        # Need the attached to UI Shapes
        destinationUmlClass: UmlClass = UmlClass(modelClass=destinationPyutClass)
        destinationUmlClass.id        = DESTINATION_UML_CLASS_ID
        destinationUmlClass.position  = UmlPosition(x=300, y=100)

        pyutNote: Note = Note(content='I am a note')
        pyutNote.id = PYUT_NOTE_ID

        sourceUmlNote: UmlNote  = UmlNote(note=pyutNote)
        sourceUmlNote.position = UmlPosition(x=300, y=200)

        sourceUmlNote.modelNote = pyutNote

        link: Link = Link(linkType=LinkType.NOTELINK)
        link.source      = pyutNote
        link.destination = destinationPyutClass

        umlNoteLink: UmlNoteLink = UmlNoteLink(link=link)
        umlNoteLink.sourceNote       = sourceUmlNote
        umlNoteLink.destinationClass = destinationUmlClass

        return CreatedNoteLink(
            destinationUmlClass=destinationUmlClass,
            sourceNote=sourceUmlNote,
            umlNoteLink=umlNoteLink
        )

    def _createClassPair(self, classCounter: int) -> Tuple[UmlClass, UmlClass]:

        sourcePyutClass:      Class = self._createSimplePyutClass(classCounter=classCounter)
        classCounter += 1
        destinationPyutClass: Class = self._createSimplePyutClass(classCounter=classCounter)

        sourcePyutClass.id      = SOURCE_PYUT_CLASS_ID
        destinationPyutClass.id = DESTINATION_PYUT_CLASS_ID

        sourceUmlClass:      UmlClass = UmlClass(modelClass=sourcePyutClass)
        destinationUmlClass: UmlClass = UmlClass(modelClass=destinationPyutClass)

        sourceUmlClass.position      = UmlPosition(x=100, y=100)
        destinationUmlClass.position = UmlPosition(x=200, y=300)

        sourceUmlClass.SetCanvas(self._diagramFrame)
        destinationUmlClass.SetCanvas(self._diagramFrame)

        sourceUmlClass.id      = SOURCE_UML_CLASS_ID
        destinationUmlClass.id = DESTINATION_UML_CLASS_ID

        return sourceUmlClass, destinationUmlClass

    def _createSimplePyutClass(self, classCounter: int) -> Class:

        className:  str   = f'GeneratedClass-{classCounter}'
        modelClass: Class = Class(name=className)

        return modelClass

    def _createAssociationPyutLink(self, pyutSource: Class, pyutDestination: Class, associationCounter: int) -> Link:

        name: str = f'Association-{associationCounter}'

        pyutLink: Link = Link(name=name, linkType=LinkType.ASSOCIATION)

        pyutLink.sourceCardinality      = 'src Card'
        pyutLink.destinationCardinality = 'dst Card'

        pyutLink.source      = pyutSource
        pyutLink.destination = pyutDestination

        return pyutLink

    def _createInheritancePyutLink(self, inheritanceCounter: int, baseUmlClass: UmlClass, subUmlClass: UmlClass) -> Link:

        name: str = f'Inheritance {inheritanceCounter}'

        pyutInheritance: Link = Link(name=name, linkType=LinkType.INHERITANCE)

        pyutInheritance.destination  = baseUmlClass.modelClass
        pyutInheritance.source       = subUmlClass.modelClass

        return pyutInheritance
