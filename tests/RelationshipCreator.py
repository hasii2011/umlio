from typing import Dict
from typing import NewType
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink
from umlshapes.frames.DiagramFrame import DiagramFrame
from umlshapes.shapes.UmlClass import UmlClass
from umlshapes.types.UmlPosition import UmlPosition

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from umlshapes.links.UmlAssociation import UmlAssociation

from umlshapes.links.UmlLink import UmlLink


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

        self._relationShips: RelationshipDescription = RelationshipDescription(
            {
                PyutLinkType.ASSOCIATION: association,
                # Identifiers.ID_DISPLAY_UML_COMPOSITION: composition,
                # Identifiers.ID_DISPLAY_UML_AGGREGATION: aggregation,
                # Identifiers.ID_DISPLAY_UML_INHERITANCE: inheritance,
                # Identifiers.ID_DISPLAY_UML_INTERFACE:   interface
            }
        )

    def createRelationship(self, linkType: PyutLinkType) -> CreatedAssociation:

        associationDescription: AssociationDescription = self._relationShips[linkType]

        # if associationDescription.linkType == PyutLinkType.INHERITANCE:
        #     self._displayUmlInheritance(associationDescription=associationDescription)
        # elif associationDescription.linkType == PyutLinkType.INTERFACE:
        #     self._displayUmlInterface(associationDescription=associationDescription)
        # else:
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

        umlAssociation.SetCanvas(self._diagramFrame)
        umlAssociation.MakeLineControlPoints(n=2)       # Make this configurable

        sourceUmlClass.addLink(umlLink=umlAssociation, destinationClass=destinationUmlClass)

        return CreatedAssociation(
            sourceUmlClass=sourceUmlClass,
            destinationUmlClass=destinationUmlClass,
            association=umlAssociation
        )

    def _createClassPair(self, classCounter: int) -> Tuple[UmlClass, UmlClass]:

        sourcePyutClass:      PyutClass = self._createSimplePyutClass(classCounter=classCounter)
        classCounter += 1
        destinationPyutClass: PyutClass = self._createSimplePyutClass(classCounter=classCounter)

        sourceUmlClass:      UmlClass = UmlClass(pyutClass=sourcePyutClass)
        destinationUmlClass: UmlClass = UmlClass(pyutClass=destinationPyutClass)

        sourceUmlClass.position      = UmlPosition(x=100, y=100)
        destinationUmlClass.position = UmlPosition(x=200, y=300)

        sourceUmlClass.SetCanvas(self._diagramFrame)
        destinationUmlClass.SetCanvas(self._diagramFrame)

        return sourceUmlClass, destinationUmlClass

    def _createSimplePyutClass(self, classCounter: int) -> PyutClass:

        className: str = f'GenerateClass-{classCounter}'
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
