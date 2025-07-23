
from typing import Dict
from typing import cast

from logging import Logger
from logging import getLogger

from umlshapes.shapes.eventhandlers.UmlClassEventHandler import UmlClassEventHandler
from wx import SHOW_EFFECT_ROLL_TO_RIGHT

from wx import Simplebook
from wx import Window

from umlshapes.UmlDiagram import UmlDiagram
from umlshapes.eventengine.UmlEventEngine import UmlEventEngine
from umlshapes.frames.UmlClassDiagramFrame import CreateLollipopCallback
from umlshapes.frames.UmlClassDiagramFrame import UmlClassDiagramFrame

from umlio.IOTypes import UmlDocument
from umlio.IOTypes import UmlDocumentTitle
from umlio.IOTypes import UmlDocuments


class DiagramManager(Simplebook):
    def __init__(self, parent: Window, umlDiagrams: UmlDocuments, umlEventEngine: UmlEventEngine):

        self.logger: Logger = getLogger(__name__)

        super().__init__(parent=parent)

        self._umlDiagrams:           UmlDocuments = umlDiagrams
        self._diagramTitleToDiagram: Dict[UmlDocumentTitle, UmlDocument] = {}
        self._diagramTitleToPage:    Dict[UmlDocumentTitle, int]        = {}

        self.SetEffect(effect=SHOW_EFFECT_ROLL_TO_RIGHT)
        for umlDiagramTitle, umlDiagram in self._umlDiagrams.items():
            diagramFrame = UmlClassDiagramFrame(
                parent=self,
                umlEventEngine=umlEventEngine,
                createLollipopCallback=cast(CreateLollipopCallback, None)
            )
            self.AddPage(diagramFrame, umlDiagramTitle)
            self._layoutShapes(diagramFrame=diagramFrame, umlDiagram=umlDiagram)
            self._diagramTitleToDiagram[umlDiagramTitle] = umlDiagram
            self._diagramTitleToPage[umlDiagramTitle]    = self.GetPageCount() - 1

    def _layoutShapes(self, diagramFrame: UmlClassDiagramFrame, umlDiagram: UmlDocument):

        for umlClass in umlDiagram.umlClasses:
            umlClass.umlFrame = diagramFrame
            diagram: UmlDiagram = diagramFrame.umlDiagram

            eventHandler: UmlClassEventHandler = UmlClassEventHandler()
            eventHandler.SetShape(umlClass)
            eventHandler.SetPreviousHandler(umlClass.GetEventHandler())
            umlClass.SetEventHandler(eventHandler)

            diagram.AddShape(umlClass)
            umlClass.Show(True)
            diagramFrame.refresh()
