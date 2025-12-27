
from typing import Dict
from typing import NewType
from typing import cast
from typing import Tuple

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from umlmodel.Link import Link
from umlmodel.Note import Note
from umlmodel.Class import Class
from umlmodel.Interface import Interface
from umlmodel.ModelTypes import ClassName

from umlmodel.enumerations.LinkType import LinkType

from umlshapes.links.UmlLink import UmlLink
from umlshapes.links.UmlNoteLink import UmlNoteLink
from umlshapes.links.UmlInterface import UmlInterface
from umlshapes.links.UmlInheritance import UmlInheritance
from umlshapes.links.UmlAssociation import UmlAssociation
from umlshapes.links.UmlLollipopInterface import UmlLollipopInterface

from umlshapes.shapes.UmlNote import UmlNote
from umlshapes.shapes.UmlClass import UmlClass

from umlshapes.frames.DiagramFrame import DiagramFrame

from umlshapes.types.Common import AttachmentSide
from umlshapes.types.UmlPosition import UmlPosition

BASE_UML_CLASS_NAME:     str = 'BaseClass'
SUBCLASS_UML_CLASS_NAME: str = 'SubClass'
BASE_UML_CLASS_ID:       str = 'call.lose.current.group'
SUBCLASS_UML_CLASS_ID:   str = 'speak.left.economic.change'
BASE_CLASS_MODEL_ID:     str = '999'
SUBCLASS_MODEL_ID:       str = '111'

SOURCE_MODEL_CLASS_ID:      str = '666'
DESTINATION_MODEL_CLASS_ID: str = '777'

SOURCE_UML_CLASS_ID:      str = 'provide.serious.hand.change'
DESTINATION_UML_CLASS_ID: str = 'believe.able.power.moment'

INTERFACE_UML_CLASS_NAME:    str = 'Interface'
IMPLEMENTING_UML_CLASS_NAME: str = 'Implementor'
INTERFACE_UML_CLASS_ID:      str = 'card.carrying.interface'
IMPLEMENTING_UML_CLASS_ID:   str = 'valley.darkness.implementor'
INTERFACE_MODEL_CLASS_ID:    str = '2222'
IMPLEMENTING_MODEL_CLASS_ID: str = '4444'

UML_LINK_CANONICAL_MONIKER: str = 'die.free.open.point'

CANONICAl_LOLLIPOP_NAME:     str            = 'IFake'
LOLLIPOP_ATTACHMENT_SIDE:    AttachmentSide = AttachmentSide.RIGHT
MODEL_INTERFACE_CANONICAL_ID: str            = '0xDEADBEEF'

DESTINATION_UML_CLASS_NAME: str = 'DestinationClass'
UML_NOTE_ID:                str = 'Note.UML.Identifier'
MODEL_NOTE_ID:              str = 'Note.Model.Identifier'
UML_NOTE_LINK_ID:           str = 'Note.Link.Identifier'


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
        sourceUmlClass, destinationUmlClass = self._createUmlClassPair(associationDescription.classCounter)
        associationDescription.classCounter += 2

        self.logger.info(f'{sourceUmlClass.id=} {destinationUmlClass.id=}')

        link: Link = self._createModelAssociationLink(sourceClass=sourceUmlClass.modelClass,
                                                      destinationClass=destinationUmlClass.modelClass,
                                                      associationCounter=associationDescription.associationCounter
                                                      )

        associationDescription.associationCounter += 1

        umlAssociation = associationDescription.associationClass(link)

        umlAssociation.id = UML_LINK_CANONICAL_MONIKER
        umlAssociation.umlFrame = self._diagramFrame
        if link.linkType != LinkType.LOLLIPOP:
            umlAssociation.MakeLineControlPoints(n=2)

        sourceUmlClass.addLink(umlLink=umlAssociation, destinationClass=destinationUmlClass)

        return CreatedLink(
            sourceUmlClass=sourceUmlClass,
            destinationUmlClass=destinationUmlClass,
            association=umlAssociation
        )

    def createUmlInheritance(self) -> CreatedLink:

        baseModelClass:     Class = Class(name=f'{BASE_UML_CLASS_NAME}')
        subClassModelClass: Class = Class(name=f'{SUBCLASS_UML_CLASS_NAME}')

        baseModelClass.id     = BASE_CLASS_MODEL_ID
        subClassModelClass.id = SUBCLASS_MODEL_ID

        baseUmlClass:     UmlClass = UmlClass(modelClass=baseModelClass)
        subClassUmlClass: UmlClass = UmlClass(modelClass=subClassModelClass)

        baseUmlClass.id     = BASE_UML_CLASS_ID
        subClassUmlClass.id = SUBCLASS_UML_CLASS_ID

        baseUmlClass.position     = UmlPosition(x=100, y=100)
        subClassUmlClass.position = UmlPosition(x=200, y=300)

        baseUmlClass.umlFrame     = self._diagramFrame
        subClassUmlClass.umlFrame = self._diagramFrame

        inheritance: Link = Link(linkType=LinkType.INHERITANCE, source=subClassModelClass, destination=baseModelClass)

        umlInheritance: UmlInheritance = UmlInheritance(link=inheritance, baseClass=baseUmlClass, subClass=subClassUmlClass)

        umlInheritance.id = UML_LINK_CANONICAL_MONIKER

        umlInheritance.umlFrame = self._diagramFrame
        umlInheritance.MakeLineControlPoints(n=2)       # Make this configurable

        umlInheritance.SetEnds(x1=0, y1=0, x2=0, y2=0)

        umlInheritance.addLineControlPoint(umlPosition=UmlPosition(x=100, y=100))
        umlInheritance.addLineControlPoint(umlPosition=UmlPosition(x=200, y=200))

        # REMEMBER:   from subclass to base class
        subClassUmlClass.addLink(umlLink=umlInheritance, destinationClass=baseUmlClass)

        return CreatedLink(
            sourceUmlClass=subClassUmlClass,
            destinationUmlClass=baseUmlClass,
            association=umlInheritance
        )

    def createUmlInterface(self) -> CreatedLink:

        interfaceModelClass:    Class = Class(name=f'{INTERFACE_UML_CLASS_NAME}')
        implementingModelClass: Class = Class(name=f'{IMPLEMENTING_UML_CLASS_NAME}')

        interfaceModelClass.id    = INTERFACE_MODEL_CLASS_ID
        implementingModelClass.id = IMPLEMENTING_MODEL_CLASS_ID

        interfaceUmlClass:    UmlClass = UmlClass(modelClass=interfaceModelClass)
        implementingUmlClass: UmlClass = UmlClass(modelClass=implementingModelClass)

        interfaceUmlClass.id    = INTERFACE_UML_CLASS_ID
        implementingUmlClass.id = IMPLEMENTING_UML_CLASS_ID

        interfaceUmlClass.position    = UmlPosition(x=3333, y=3333)
        implementingUmlClass.position = UmlPosition(x=4444, y=4444)

        interfaceUmlClass.umlFrame    = self._diagramFrame
        implementingUmlClass.umlFrame = self._diagramFrame

        interface: Link = Link(linkType=LinkType.INTERFACE, source=implementingModelClass, destination=interfaceModelClass)

        umlInterface: UmlInterface = UmlInterface(link=interface, interfaceClass=interfaceUmlClass, implementingClass=implementingUmlClass)

        umlInterface.id = UML_LINK_CANONICAL_MONIKER

        umlInterface.umlFrame = self._diagramFrame
        umlInterface.MakeLineControlPoints(n=2)       # Make this configurable

        umlInterface.addLineControlPoint(umlPosition=UmlPosition(x=372, y=433))
        umlInterface.addLineControlPoint(umlPosition=UmlPosition(x=400, y=433))

        # REMEMBER:   from subclass to base class
        implementingUmlClass.addLink(umlLink=umlInterface, destinationClass=interfaceUmlClass)

        return CreatedLink(
            sourceUmlClass=implementingUmlClass,
            destinationUmlClass=interfaceUmlClass,
            association=umlInterface
        )

    def createLollipop(self):

        # Need the model
        implementingModelClass: Class = Class(name=f'{IMPLEMENTING_UML_CLASS_NAME}')
        implementingModelClass.id = IMPLEMENTING_MODEL_CLASS_ID

        # Need the attached to UI Shape
        implementingUmlClass: UmlClass = UmlClass(modelClass=implementingModelClass)
        implementingUmlClass.id       = IMPLEMENTING_UML_CLASS_ID
        implementingUmlClass.position = UmlPosition(x=3333, y=3333)

        # fill out the model
        interface: Interface = Interface(name=CANONICAl_LOLLIPOP_NAME)
        interface.id = MODEL_INTERFACE_CANONICAL_ID
        interface.addImplementor(ClassName(implementingModelClass.name))

        # Need the lollipop
        umlLollipopInterface: UmlLollipopInterface = UmlLollipopInterface(interface=interface)
        umlLollipopInterface.attachedTo     = implementingUmlClass
        umlLollipopInterface.attachmentSide = LOLLIPOP_ATTACHMENT_SIDE

        return umlLollipopInterface, implementingUmlClass

    def createNoteLink(self) -> CreatedNoteLink:

        # Need the model
        destinationClass: Class = Class(name=f'{DESTINATION_UML_CLASS_NAME}')
        destinationClass.id = DESTINATION_MODEL_CLASS_ID

        # Need the attached to UI Shapes
        destinationUmlClass: UmlClass = UmlClass(modelClass=destinationClass)
        destinationUmlClass.id        = DESTINATION_UML_CLASS_ID
        destinationUmlClass.position  = UmlPosition(x=300, y=100)

        note: Note = Note(content='I am a note')
        note.id = MODEL_NOTE_ID

        sourceUmlNote: UmlNote  = UmlNote(note=note)
        sourceUmlNote.id       = UML_NOTE_ID
        sourceUmlNote.position = UmlPosition(x=300, y=200)
        sourceUmlNote.modelNote = note

        modelLink: Link = Link(linkType=LinkType.NOTELINK)
        modelLink.source      = note
        modelLink.destination = destinationClass

        umlNoteLink: UmlNoteLink = UmlNoteLink(link=modelLink)
        umlNoteLink.id               = UML_NOTE_LINK_ID
        umlNoteLink.sourceNote       = sourceUmlNote
        umlNoteLink.destinationClass = destinationUmlClass

        umlNoteLink.addLineControlPoint(umlPosition=UmlPosition(x=372, y=433))
        umlNoteLink.addLineControlPoint(umlPosition=UmlPosition(x=400, y=433))

        sourceUmlNote.umlFrame = self._diagramFrame
        sourceUmlNote.addLink(umlNoteLink=umlNoteLink, umlClass=destinationUmlClass)

        return CreatedNoteLink(
            destinationUmlClass=destinationUmlClass,
            sourceNote=sourceUmlNote,
            umlNoteLink=umlNoteLink
        )

    def _createUmlClassPair(self, classCounter: int) -> Tuple[UmlClass, UmlClass]:

        sourceClass:      Class = self._createSimpleModelClass(classCounter=classCounter)
        classCounter += 1
        destinationClass: Class = self._createSimpleModelClass(classCounter=classCounter)

        sourceClass.id      = SOURCE_MODEL_CLASS_ID
        destinationClass.id = DESTINATION_MODEL_CLASS_ID

        sourceUmlClass:      UmlClass = UmlClass(modelClass=sourceClass)
        destinationUmlClass: UmlClass = UmlClass(modelClass=destinationClass)

        sourceUmlClass.position      = UmlPosition(x=100, y=100)
        destinationUmlClass.position = UmlPosition(x=200, y=300)

        sourceUmlClass.umlFrame      = self._diagramFrame
        sourceUmlClass.umlFrame      = self._diagramFrame
        destinationUmlClass.umlFrame = self._diagramFrame

        sourceUmlClass.id      = SOURCE_UML_CLASS_ID
        destinationUmlClass.id = DESTINATION_UML_CLASS_ID

        return sourceUmlClass, destinationUmlClass

    def _createSimpleModelClass(self, classCounter: int) -> Class:

        className:  str   = f'GeneratedClass-{classCounter}'
        modelClass: Class = Class(name=className)

        return modelClass

    def _createModelAssociationLink(self, sourceClass: Class, destinationClass: Class, associationCounter: int) -> Link:

        name: str = f'Association-{associationCounter}'

        link: Link = Link(name=name, linkType=LinkType.ASSOCIATION)

        link.sourceCardinality      = 'src Card'
        link.destinationCardinality = 'dst Card'

        link.source      = sourceClass
        link.destination = destinationClass

        return link

    def _createModelInheritanceLink(self, inheritanceCounter: int, baseUmlClass: UmlClass, subUmlClass: UmlClass) -> Link:

        name: str = f'Inheritance {inheritanceCounter}'

        inheritance: Link = Link(name=name, linkType=LinkType.INHERITANCE)

        inheritance.destination  = baseUmlClass.modelClass
        inheritance.source       = subUmlClass.modelClass

        return inheritance
