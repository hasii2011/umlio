
from typing import Dict
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from wx import SHOW_EFFECT_ROLL_TO_RIGHT

from wx import Simplebook
from wx import Window

from umlshapes.shapes.eventhandlers.UmlClassEventHandler import UmlClassEventHandler

from umlshapes.UmlDiagram import UmlDiagram

from umlshapes.eventengine.UmlEventEngine import UmlEventEngine

from umlshapes.frames.DiagramFrame import FrameId
from umlshapes.frames.UmlClassDiagramFrame import CreateLollipopCallback
from umlshapes.frames.UmlClassDiagramFrame import UmlClassDiagramFrame

from umlio.IOTypes import UmlDocument
from umlio.IOTypes import UmlDocumentTitle
from umlio.IOTypes import UmlDocuments

FrameIdToUmlDocument = NewType('FrameIdToUmlDocument', Dict[FrameId, UmlDocument])
UmlDocumentToPage    = NewType('UmlDocumentToPage', Dict[UmlDocumentTitle, int])


class DiagramManager(Simplebook):
    def __init__(self, parent: Window, umlDocuments: UmlDocuments, umlEventEngine: UmlEventEngine):
        """

        Args:
            parent:             Parent window
            umlDocuments:       UmlDocuments the diagram manager will switch between
            umlEventEngine:     The Uml Event engine, In case something happens on the diagram frame
        """

        self.logger: Logger = getLogger(__name__)

        super().__init__(parent=parent)

        self._umlDocuments:   UmlDocuments   = umlDocuments
        self._umlEventEngine: UmlEventEngine = umlEventEngine

        self._diagramTitleToDiagram: FrameIdToUmlDocument = FrameIdToUmlDocument({})
        self._diagramTitleToPage:    UmlDocumentToPage    = UmlDocumentToPage({})

        self.SetEffect(effect=SHOW_EFFECT_ROLL_TO_RIGHT)                # TODO:  Should be an application preference
        self.SetEffectTimeout(timeout=100)                              # TODO:  Should be an application preference

        self._createPages()

        self.SetSelection(0)

    def _createPages(self):

        for umlDocumentTitle, umlDocument in self._umlDocuments.items():
            diagramFrame = UmlClassDiagramFrame(
                parent=self,
                umlEventEngine=self._umlEventEngine,
                createLollipopCallback=cast(CreateLollipopCallback, None)       # TODO:  Where is this
            )
            self.AddPage(diagramFrame, umlDocumentTitle)
            self._layoutShapes(diagramFrame=diagramFrame, umlDiagram=umlDocument)

            self._diagramTitleToDiagram[diagramFrame.id] = umlDocument
            self._diagramTitleToPage[umlDocumentTitle] = self.GetPageCount() - 1

    def setPage(self, umlDocumentTitle: UmlDocumentTitle):
        self.SetSelection(self._diagramTitleToPage[umlDocumentTitle])

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
