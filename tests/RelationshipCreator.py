
from typing import Dict
from typing import NewType
from typing import cast
from typing import Tuple

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutModelTypes import ClassName
from umlshapes.links.UmlLollipopInterface import UmlLollipopInterface
from umlshapes.types.Common import AttachmentSide

from wx import Point

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

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
BASE_CLASS_PYUT_ID:      int = 999
SUBCLASS_PYUT_ID:        int = 111

SOURCE_PYUT_CLASS_ID:      int = 666
DESTINATION_PYUT_CLASS_ID: int = 777

SOURCE_UML_CLASS_ID:      str = 'provide.serious.hand.change'
DESTINATION_UML_CLASS_ID: str = 'believe.able.power.moment'

INTERFACE_UML_CLASS_NAME:    str = 'Interface'
IMPLEMENTING_UML_CLASS_NAME: str = 'Implementor'
INTERFACE_UML_CLASS_ID:      str = 'card.carrying.interface'
IMPLEMENTING_UML_CLASS_ID:   str = 'valley.darkness.implementor'
INTERFACE_PYUT_CLASS_ID:     int = 2222
IMPLEMENTING_PYUT_CLASS_ID:  int = 4444

UML_LINK_CANONICAL_MONIKER: str = 'die.free.open.point'

CANONICAl_LOLLIPOP_NAME:     str            = 'IFake'
LOLLIPOP_ATTACHMENT_SIDE:    AttachmentSide = AttachmentSide.RIGHT
PYUT_INTERFACE_CANONICAL_ID: int            = 0xDEADBEEF


@dataclass
class AssociationDescription:
    associationClass:   type[UmlLink] | type[UmlLollipopInterface]
    linkType:           PyutLinkType  = PyutLinkType.ASSOCIATION
    associationCounter: int = 0
    classCounter:       int = 0


RelationshipDescription = NewType('RelationshipDescription', Dict[PyutLinkType, AssociationDescription])


@dataclass
class CreatedAssociation:
    sourceUmlClass:      UmlClass             = cast(UmlClass, None)
    association:         UmlLink              = cast(UmlLink, None)
    destinationUmlClass: UmlClass             = cast(UmlClass, None)
    lollipopInterface:   UmlLollipopInterface = cast(UmlLollipopInterface, None)


class RelationshipCreator:
    def __init__(self, diagramFrame: DiagramFrame):
        self.logger: Logger = getLogger(__name__)

        self._diagramFrame: DiagramFrame = diagramFrame

        association: AssociationDescription = AssociationDescription(
            linkType=PyutLinkType.ASSOCIATION,
            associationClass=UmlAssociation
        )
        inheritance: AssociationDescription = AssociationDescription(
            linkType=PyutLinkType.INHERITANCE,
            associationClass=UmlInheritance
        )
        interface: AssociationDescription = AssociationDescription(
            linkType=PyutLinkType.INTERFACE,
            associationClass=UmlInterface
        )
        lollipop: AssociationDescription = AssociationDescription(
            linkType=PyutLinkType.LOLLIPOP,
            associationClass=UmlLollipopInterface
        )
        self._relationShips: RelationshipDescription = RelationshipDescription(
            {
                PyutLinkType.ASSOCIATION: association,
                PyutLinkType.INHERITANCE: inheritance,
                PyutLinkType.INTERFACE:   interface,
                PyutLinkType.LOLLIPOP:    lollipop,
                # Identifiers.ID_DISPLAY_UML_COMPOSITION: composition,
                # Identifiers.ID_DISPLAY_UML_AGGREGATION: aggregation,
            }
        )

    # noinspection PyTypeChecker
    def createRelationship(self, linkType: PyutLinkType) -> CreatedAssociation:

        associationDescription: AssociationDescription = self._relationShips[linkType]

        if associationDescription.linkType == PyutLinkType.INHERITANCE:
            return self._createUmlInheritance(associationDescription=associationDescription)
        elif associationDescription.linkType == PyutLinkType.INTERFACE:
            return self._createUmlInterface()
        elif associationDescription.linkType == PyutLinkType.LOLLIPOP:
            return self._createLollipop()
        else:
            return self._createAssociation(associationDescription=associationDescription)

    def _createAssociation(self, associationDescription: AssociationDescription) -> CreatedAssociation:
        """

        Args:
            associationDescription:
        """
        sourceUmlClass, destinationUmlClass = self._createClassPair(associationDescription.classCounter)
        associationDescription.classCounter += 2

        self.logger.info(f'{sourceUmlClass.id=} {destinationUmlClass.id=}')

        pyutLink = self._createAssociationPyutLink(pyutSource=sourceUmlClass.pyutClass,
                                                   pyutDestination=destinationUmlClass.pyutClass,
                                                   associationCounter=associationDescription.associationCounter
                                                   )

        associationDescription.associationCounter += 1

        umlAssociation = associationDescription.associationClass(pyutLink)      # type: ignore

        umlAssociation.id = UML_LINK_CANONICAL_MONIKER
        umlAssociation.SetCanvas(self._diagramFrame)
        umlAssociation.MakeLineControlPoints(n=2)       # Make this configurable

        sourceUmlClass.addLink(umlLink=umlAssociation, destinationClass=destinationUmlClass)

        return CreatedAssociation(
            sourceUmlClass=sourceUmlClass,
            destinationUmlClass=destinationUmlClass,
            association=umlAssociation
        )

    def _createUmlInheritance(self, associationDescription: AssociationDescription) -> CreatedAssociation:

        basePyutClass: PyutClass = PyutClass(name=f'{BASE_UML_CLASS_NAME}')
        associationDescription.classCounter += 1
        subPyutClass: PyutClass = PyutClass(name=f'{SUBCLASS_UML_CLASS_NAME}')

        basePyutClass.id = BASE_CLASS_PYUT_ID
        subPyutClass.id  = SUBCLASS_PYUT_ID

        baseUmlClass:     UmlClass = UmlClass(pyutClass=basePyutClass)
        subClassUmlClass: UmlClass = UmlClass(pyutClass=subPyutClass)

        baseUmlClass.name     = BASE_UML_CLASS_NAME
        subClassUmlClass.name = SUBCLASS_UML_CLASS_NAME
        baseUmlClass.id       = BASE_UML_CLASS_ID
        subClassUmlClass.id   = SUBCLASS_UML_CLASS_ID

        baseUmlClass.position     = UmlPosition(x=100, y=100)
        subClassUmlClass.position = UmlPosition(x=200, y=300)

        baseUmlClass.SetCanvas(self._diagramFrame)
        subClassUmlClass.SetCanvas(self._diagramFrame)

        pyutInheritance: PyutLink = PyutLink(linkType=PyutLinkType.INHERITANCE, source=subPyutClass, destination=basePyutClass)

        umlInheritance: UmlInheritance = UmlInheritance(pyutLink=pyutInheritance, baseClass=baseUmlClass, subClass=subClassUmlClass)

        umlInheritance.id = UML_LINK_CANONICAL_MONIKER

        umlInheritance.SetCanvas(self._diagramFrame)
        umlInheritance.MakeLineControlPoints(n=2)       # Make this configurable

        umlInheritance.InsertLineControlPoint(point=Point(x=100, y=100))
        umlInheritance.InsertLineControlPoint(point=Point(x=200, y=200))

        # REMEMBER:   from subclass to base class
        subClassUmlClass.addLink(umlLink=umlInheritance, destinationClass=baseUmlClass)

        return CreatedAssociation(
            sourceUmlClass=subClassUmlClass,
            destinationUmlClass=baseUmlClass,
            association=umlInheritance
        )

    def _createUmlInterface(self) -> CreatedAssociation:

        interfacePyutClass:    PyutClass = PyutClass(name=f'{INTERFACE_UML_CLASS_NAME}')
        implementingPyutClass: PyutClass = PyutClass(name=f'{IMPLEMENTING_UML_CLASS_NAME}')

        interfacePyutClass.id    = INTERFACE_PYUT_CLASS_ID
        implementingPyutClass.id = IMPLEMENTING_PYUT_CLASS_ID

        interfaceUmlClass:    UmlClass = UmlClass(pyutClass=interfacePyutClass)
        implementingUmlClass: UmlClass = UmlClass(pyutClass=implementingPyutClass)

        interfaceUmlClass.id    = INTERFACE_UML_CLASS_ID
        implementingUmlClass.id = IMPLEMENTING_UML_CLASS_ID

        interfaceUmlClass.position    = UmlPosition(x=3333, y=3333)
        implementingUmlClass.position = UmlPosition(x=4444, y=4444)

        interfaceUmlClass.SetCanvas(self._diagramFrame)
        implementingUmlClass.SetCanvas(self._diagramFrame)

        pyutInterface: PyutLink = PyutLink(linkType=PyutLinkType.INTERFACE, source=implementingPyutClass, destination=interfacePyutClass)     # TODO use PyutInterface

        umlInterface: UmlInterface = UmlInterface(pyutLink=pyutInterface, interfaceClass=interfaceUmlClass, implementingClass=implementingUmlClass)

        umlInterface.id = UML_LINK_CANONICAL_MONIKER

        umlInterface.SetCanvas(self._diagramFrame)
        umlInterface.MakeLineControlPoints(n=2)       # Make this configurable

        umlInterface.InsertLineControlPoint(point=Point(x=372, y=433))
        umlInterface.InsertLineControlPoint(point=Point(x=400, y=433))

        # REMEMBER:   from subclass to base class
        implementingUmlClass.addLink(umlLink=umlInterface, destinationClass=interfaceUmlClass)

        return CreatedAssociation(
            sourceUmlClass=implementingUmlClass,
            destinationUmlClass=interfaceUmlClass,
            association=umlInterface
        )

    def _createLollipop(self) -> CreatedAssociation:

        # Need them model
        implementingPyutClass: PyutClass = PyutClass(name=f'{IMPLEMENTING_UML_CLASS_NAME}')
        implementingPyutClass.id = IMPLEMENTING_PYUT_CLASS_ID

        # Need the attached to UI Shape
        implementingUmlClass: UmlClass = UmlClass(pyutClass=implementingPyutClass)
        implementingUmlClass.id       = IMPLEMENTING_UML_CLASS_ID
        implementingUmlClass.position = UmlPosition(x=3333, y=3333)

        # fill out the model
        pyutInterface: PyutInterface = PyutInterface(name=CANONICAl_LOLLIPOP_NAME)
        pyutInterface.id = PYUT_INTERFACE_CANONICAL_ID
        pyutInterface.addImplementor(ClassName(implementingPyutClass.name))

        # Need the lollipop
        umlLollipopInterface: UmlLollipopInterface = UmlLollipopInterface(pyutInterface=pyutInterface)
        umlLollipopInterface.attachedTo     = implementingUmlClass
        umlLollipopInterface.attachmentSide = LOLLIPOP_ATTACHMENT_SIDE
        return CreatedAssociation(
            destinationUmlClass=implementingUmlClass,
            lollipopInterface=umlLollipopInterface
        )

    def _createClassPair(self, classCounter: int) -> Tuple[UmlClass, UmlClass]:

        sourcePyutClass:      PyutClass = self._createSimplePyutClass(classCounter=classCounter)
        classCounter += 1
        destinationPyutClass: PyutClass = self._createSimplePyutClass(classCounter=classCounter)

        sourcePyutClass.id      = SOURCE_PYUT_CLASS_ID
        destinationPyutClass.id = DESTINATION_PYUT_CLASS_ID

        sourceUmlClass:      UmlClass = UmlClass(pyutClass=sourcePyutClass)
        destinationUmlClass: UmlClass = UmlClass(pyutClass=destinationPyutClass)

        sourceUmlClass.position      = UmlPosition(x=100, y=100)
        destinationUmlClass.position = UmlPosition(x=200, y=300)

        sourceUmlClass.SetCanvas(self._diagramFrame)
        destinationUmlClass.SetCanvas(self._diagramFrame)

        sourceUmlClass.id      = SOURCE_UML_CLASS_ID
        destinationUmlClass.id = DESTINATION_UML_CLASS_ID

        return sourceUmlClass, destinationUmlClass

    def _createSimplePyutClass(self, classCounter: int) -> PyutClass:

        className: str = f'GeneratedClass-{classCounter}'
        pyutClass: PyutClass  = PyutClass(name=className)

        return pyutClass

    def _createAssociationPyutLink(self, pyutSource: PyutClass, pyutDestination: PyutClass, associationCounter: int) -> PyutLink:

        name: str = f'Association-{associationCounter}'

        pyutLink: PyutLink = PyutLink(name=name, linkType=PyutLinkType.ASSOCIATION)

        pyutLink.sourceCardinality      = 'src Card'
        pyutLink.destinationCardinality = 'dst Card'

        pyutLink.source      = pyutSource
        pyutLink.destination = pyutDestination

        return pyutLink

    def _createInheritancePyutLink(self, inheritanceCounter: int, baseUmlClass: UmlClass, subUmlClass: UmlClass) -> PyutLink:

        name: str = f'Inheritance {inheritanceCounter}'

        pyutInheritance: PyutLink = PyutLink(name=name, linkType=PyutLinkType.INHERITANCE)

        pyutInheritance.destination  = baseUmlClass.pyutClass
        pyutInheritance.source       = subUmlClass.pyutClass

        return pyutInheritance
