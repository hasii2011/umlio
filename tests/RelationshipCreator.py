from typing import Dict
from typing import NewType
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import Point

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

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


UML_LINK_CANONICAL_MONIKER: str = 'die.free.open.point'


@dataclass
class AssociationDescription:
    associationClass:   type[UmlLink] = cast(type[UmlLink], None)
    linkType:           PyutLinkType  = PyutLinkType.ASSOCIATION
    associationCounter: int = 0
    classCounter:       int = 0


RelationshipDescription = NewType('RelationshipDescription', Dict[PyutLinkType, AssociationDescription])


@dataclass
class CreatedAssociation:
    sourceUmlClass:      UmlClass
    destinationUmlClass: UmlClass
    association:         UmlLink


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

        self._relationShips: RelationshipDescription = RelationshipDescription(
            {
                PyutLinkType.ASSOCIATION: association,
                PyutLinkType.INHERITANCE: inheritance,
                # Identifiers.ID_DISPLAY_UML_COMPOSITION: composition,
                # Identifiers.ID_DISPLAY_UML_AGGREGATION: aggregation,
                # Identifiers.ID_DISPLAY_UML_INTERFACE:   interface
            }
        )

    def createRelationship(self, linkType: PyutLinkType) -> CreatedAssociation:

        associationDescription: AssociationDescription = self._relationShips[linkType]

        if associationDescription.linkType == PyutLinkType.INHERITANCE:
            return self._createUmlInheritance(associationDescription=associationDescription)
        # elif associationDescription.linkType == PyutLinkType.INTERFACE:
        #     self._displayUmlInterface(associationDescription=associationDescription)
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

        umlAssociation = associationDescription.associationClass(pyutLink=pyutLink)

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

        basePyutClass: PyutClass = PyutClass(name=f'BaseClass')
        associationDescription.classCounter += 1
        subPyutClass: PyutClass = PyutClass(name=f'SubClass')

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
