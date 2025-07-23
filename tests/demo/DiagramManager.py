
from logging import Logger
from logging import getLogger
from typing import Dict
from typing import cast

from umlshapes.eventengine.UmlEventEngine import UmlEventEngine
from umlshapes.frames.UmlClassDiagramFrame import CreateLollipopCallback
from umlshapes.frames.UmlClassDiagramFrame import UmlClassDiagramFrame

from wx import SHOW_EFFECT_ROLL_TO_RIGHT

from wx import Simplebook
from wx import Window

from umlio.IOTypes import UmlDiagram
from umlio.IOTypes import UmlDiagramTitle
from umlio.IOTypes import UmlDiagrams


class DiagramManager(Simplebook):
    def __init__(self, parent: Window, umlDiagrams: UmlDiagrams, umlEventEngine: UmlEventEngine):

        self.logger: Logger = getLogger(__name__)

        super().__init__(parent=parent)

        self._umlDiagrams:           UmlDiagrams = umlDiagrams
        self._diagramTitleToDiagram: Dict[UmlDiagramTitle, UmlDiagram] = {}
        self._diagramTitleToPage:    Dict[UmlDiagramTitle, int]        = {}

        self.SetEffect(effect=SHOW_EFFECT_ROLL_TO_RIGHT)
        for umlDiagramTitle, umlDiagram in self._umlDiagrams.items():
            diagramFrame = UmlClassDiagramFrame(
                parent=self,
                umlEventEngine=umlEventEngine,
                createLollipopCallback=cast(CreateLollipopCallback, None)
            )
            self.AddPage(diagramFrame, umlDiagramTitle)
            self._diagramTitleToDiagram[umlDiagramTitle] = umlDiagram
            self._diagramTitleToPage[umlDiagramTitle]    = self.GetPageCount() - 1
