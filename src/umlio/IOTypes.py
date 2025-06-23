
from typing import Dict
from typing import List
from typing import NewType

from enum import Enum

from dataclasses import dataclass
from dataclasses import field

from pathlib import Path

from umlshapes.shapes.UmlClass import UmlClass

UML_VERSION: str = '12.0'

UmlDiagramTitle = NewType('UmlDiagramTitle', str)
UmlClasses      = NewType('UmlClasses',      List[UmlClass])

ElementAttributes = NewType('ElementAttributes', Dict[str, str])


class UmlDiagramType(Enum):
    CLASS_DIAGRAM    = 'Class Diagram'
    USE_CASE_DIAGRAM = 'Use Case Diagram'
    SEQUENCE_DIAGRAM = 'Sequence Diagram'
    NOT_SET          = 'Not Set'


def createUmlClassesFactory() -> UmlClasses:
    """
    Factory method to create  the UmlClasses data structure;

    Returns:  A new data structure
    """
    return UmlClasses([])


@dataclass
class UmlDiagram:
    diagramType:     UmlDiagramType  = UmlDiagramType.NOT_SET
    diagramTitle:    UmlDiagramTitle = UmlDiagramTitle('')
    scrollPositionX: int = 1
    scrollPositionY: int = 1
    pixelsPerUnitX:  int = 1
    pixelsPerUnitY:  int = 1
    umlClasses:      UmlClasses  = field(default_factory=createUmlClassesFactory)


UmlDiagrams = NewType('UmlDiagrams', Dict[UmlDiagramTitle, UmlDiagram])


def createUmlDiagramsFactory() -> UmlDiagrams:
    return UmlDiagrams({})


@dataclass
class UmlProject:
    fileName:    str  = ''
    version:     str  = UML_VERSION
    codePath:    Path = Path('')
    umlDiagrams: UmlDiagrams = field(default_factory=createUmlDiagramsFactory)
