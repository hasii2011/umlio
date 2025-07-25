
from typing import Dict
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine
from wx import SHOW_EFFECT_SLIDE_TO_RIGHT

from wx import Simplebook
from wx import Window

from wx.lib.ogl import ShapeEvtHandler

from umlshapes.frames.DiagramFrame import FrameId
from umlshapes.frames.ClassDiagramFrame import ClassDiagramFrame
from umlshapes.frames.ClassDiagramFrame import CreateLollipopCallback
from umlshapes.frames.SequenceDiagramFrame import SequenceDiagramFrame
from umlshapes.frames.UseCaseDiagramFrame import UseCaseDiagramFrame

from umlshapes.shapes.eventhandlers.UmlClassEventHandler import UmlClassEventHandler
from umlshapes.shapes.eventhandlers.UmlActorEventHandler import UmlActorEventHandler
from umlshapes.shapes.eventhandlers.UmlNoteEventHandler import UmlNoteEventHandler
from umlshapes.shapes.eventhandlers.UmlTextEventHandler import UmlTextEventHandler
from umlshapes.shapes.eventhandlers.UmlUseCaseEventHandler import UmlUseCaseEventHandler

from umlshapes.shapes.UmlActor import UmlActor
from umlshapes.shapes.UmlClass import UmlClass
from umlshapes.shapes.UmlNote import UmlNote
from umlshapes.shapes.UmlText import UmlText
from umlshapes.shapes.UmlUseCase import UmlUseCase

from umlshapes.UmlDiagram import UmlDiagram

from umlio.IOTypes import UmlActors
from umlio.IOTypes import UmlClasses
from umlio.IOTypes import UmlDocument
from umlio.IOTypes import UmlDocumentTitle
from umlio.IOTypes import UmlDocumentType
from umlio.IOTypes import UmlDocuments
from umlio.IOTypes import UmlNotes
from umlio.IOTypes import UmlTexts
from umlio.IOTypes import UmlUseCases

FrameIdToUmlDocument = NewType('FrameIdToUmlDocument', Dict[FrameId, UmlDocument])
UmlDocumentToPage    = NewType('UmlDocumentToPage', Dict[UmlDocumentTitle, int])

UmlShape = UmlActor | UmlNote | UmlText | UmlUseCase | UmlClass


class DiagramManager(Simplebook):
    def __init__(self, parent: Window, umlDocuments: UmlDocuments, umlPubSubEngine: UmlPubSubEngine):
        """

        Args:
            parent:             Parent window
            umlDocuments:       UmlDocuments the diagram manager will switch between
            umlPubSubEngine:     The Uml Event engine, In case something happens on the diagram frame
        """

        self.logger: Logger = getLogger(__name__)

        super().__init__(parent=parent)

        self._umlDocuments:    UmlDocuments    = umlDocuments
        self._umlPubSubEngine: UmlPubSubEngine = umlPubSubEngine

        self._diagramTitleToDiagram: FrameIdToUmlDocument = FrameIdToUmlDocument({})
        self._diagramTitleToPage:    UmlDocumentToPage    = UmlDocumentToPage({})

        self.SetEffect(effect=SHOW_EFFECT_SLIDE_TO_RIGHT)               # TODO:  Should be an application preference
        self.SetEffectTimeout(timeout=200)                              # TODO:  Should be an application preference

        self._createPages()

        self.SetSelection(0)

    def setPage(self, umlDocumentTitle: UmlDocumentTitle):
        self.SetSelection(self._diagramTitleToPage[umlDocumentTitle])

    def _createPages(self):

        for umlDocumentTitle, umlDocument in self._umlDocuments.items():

            documentType: UmlDocumentType = umlDocument.documentType

            if documentType == UmlDocumentType.CLASS_DOCUMENT:
                diagramFrame = ClassDiagramFrame(
                    parent=self,
                    umlPubSubEngine=self._umlPubSubEngine,
                    createLollipopCallback=cast(CreateLollipopCallback, None)       # TODO:  Where is this
                )
            elif documentType == UmlDocumentType.USE_CASE_DOCUMENT:
                diagramFrame = UseCaseDiagramFrame(
                    parent=self,
                    umlPubSubEngine=self._umlPubSubEngine,
                )
            elif documentType == UmlDocumentType.SEQUENCE_DOCUMENT:
                diagramFrame = SequenceDiagramFrame(
                    parent=self,
                    umlPubSubEngine=self._umlPubSubEngine
                )
            else:
                assert False, f'Unknown UML document type: {documentType=}'

            self.AddPage(diagramFrame, umlDocumentTitle)
            self._layoutShapes(diagramFrame=diagramFrame, umlDocument=umlDocument)

            self._diagramTitleToDiagram[diagramFrame.id] = umlDocument
            self._diagramTitleToPage[umlDocumentTitle] = self.GetPageCount() - 1

    def _layoutShapes(self, diagramFrame: ClassDiagramFrame | UseCaseDiagramFrame, umlDocument: UmlDocument):

        self._layoutClasses(diagramFrame, umlDocument.umlClasses)
        self._layoutNotes(diagramFrame, umlDocument.umlNotes)
        self._layoutTexts(diagramFrame, umlDocument.umlTexts)
        self._layoutActors(diagramFrame, umlDocument.umlActors)
        self._layoutUseCases(diagramFrame, umlDocument.umlUseCases)

    def _layoutClasses(self, diagramFrame: ClassDiagramFrame, umlClasses: UmlClasses):
        for umlClass in umlClasses:
            self._layoutShape(
                umlShape=umlClass,
                diagramFrame=diagramFrame,
                eventHandlerClass=UmlClassEventHandler
            )

    def _layoutNotes(self, diagramFrame: ClassDiagramFrame | UseCaseDiagramFrame, umlNotes: UmlNotes):

        for umlNote in umlNotes:
            self._layoutShape(
                umlShape=umlNote,
                diagramFrame=diagramFrame,
                eventHandlerClass=UmlNoteEventHandler
            )

    def _layoutTexts(self, diagramFrame: ClassDiagramFrame, umlTexts: UmlTexts):

        for umlText in umlTexts:
            self._layoutShape(
                umlShape=umlText,
                diagramFrame=diagramFrame,
                eventHandlerClass=UmlTextEventHandler
            )

    def _layoutActors(self, diagramFrame: UseCaseDiagramFrame, umlActors: UmlActors):

        for umlActor in umlActors:
            self._layoutShape(
                umlShape=umlActor,
                diagramFrame=diagramFrame,
                eventHandlerClass=UmlActorEventHandler
            )

    def _layoutUseCases(self, diagramFrame: UseCaseDiagramFrame, umlUseCases: UmlUseCases):
        for umlUseCase in umlUseCases:
            self._layoutShape(
                umlShape=umlUseCase,
                diagramFrame=diagramFrame,
                eventHandlerClass=UmlUseCaseEventHandler
            )

    def _layoutShape(self, umlShape: UmlShape, diagramFrame: ClassDiagramFrame | UseCaseDiagramFrame, eventHandlerClass: type[ShapeEvtHandler]):
        """

        Args:
            umlShape:
            diagramFrame:
            eventHandlerClass:
        """

        umlShape.umlFrame = diagramFrame
        diagram: UmlDiagram = diagramFrame.umlDiagram

        eventHandler: ShapeEvtHandler = eventHandlerClass()
        eventHandler.SetShape(umlShape)
        eventHandler.SetPreviousHandler(umlShape.GetEventHandler())
        umlShape.SetEventHandler(eventHandler)

        diagram.AddShape(umlShape)
        umlShape.Show(True)

        diagramFrame.refresh()
