
from typing import Dict
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Window
from wx import Simplebook
from wx import ClientDC

from umlshapes.frames.DiagramFrame import DiagramFrame
from umlshapes.frames.DiagramFrame import FrameId
from umlshapes.frames.ClassDiagramFrame import ClassDiagramFrame
from umlshapes.frames.SequenceDiagramFrame import SequenceDiagramFrame
from umlshapes.frames.UseCaseDiagramFrame import UseCaseDiagramFrame
from umlshapes.frames.UmlFrame import UmlFrame

from umlshapes.types.UmlPosition import UmlPosition

from umlshapes.UmlDiagram import UmlDiagram
from umlshapes.UmlBaseEventHandler import UmlBaseEventHandler
from umlshapes.ShapeTypes import UmlShapes

from umlshapes.shapes.UmlNote import UmlNote
from umlshapes.shapes.UmlText import UmlText
from umlshapes.shapes.UmlActor import UmlActor
from umlshapes.shapes.UmlClass import UmlClass
from umlshapes.shapes.UmlUseCase import UmlUseCase
from umlshapes.shapes.UmlControlPoint import UmlControlPoint

from umlshapes.shapes.eventhandlers.UmlNoteEventHandler import UmlNoteEventHandler
from umlshapes.shapes.eventhandlers.UmlTextEventHandler import UmlTextEventHandler
from umlshapes.shapes.eventhandlers.UmlActorEventHandler import UmlActorEventHandler
from umlshapes.shapes.eventhandlers.UmlClassEventHandler import UmlClassEventHandler
from umlshapes.shapes.eventhandlers.UmlUseCaseEventHandler import UmlUseCaseEventHandler

from umlshapes.links.UmlLink import UmlLink
from umlshapes.links.UmlNoteLink import UmlNoteLink
from umlshapes.links.UmlInterface import UmlInterface
from umlshapes.links.UmlAssociation import UmlAssociation
from umlshapes.links.UmlInheritance import UmlInheritance
from umlshapes.links.UmlComposition import UmlComposition
from umlshapes.links.UmlAggregation import UmlAggregation
from umlshapes.links.UmlLollipopInterface import UmlLollipopInterface

from umlshapes.links.eventhandlers.UmlLinkEventHandler import UmlLinkEventHandler
from umlshapes.links.eventhandlers.UmlNoteLinkEventHandler import UmlNoteLinkEventHandler
from umlshapes.links.eventhandlers.UmlAssociationEventHandler import UmlAssociationEventHandler
from umlshapes.links.eventhandlers.UmlLollipopInterfaceEventHandler import UmlLollipopInterfaceEventHandler

from umlshapes.sd.UmlSDCombinedFragment import UmlSDCombinedFragment
from umlshapes.sd.UmlSDExecution import UmlSDExecution
from umlshapes.sd.UmlSDInstance import UmlSDInstance
from umlshapes.sd.UmlSDMessage import UmlSDMessage

from umlshapes.sd.eventhandlers.UmlSDCombinedFragmentEventHandler import UmlSDCombinedFragmentEventHandler
from umlshapes.sd.eventhandlers.UmlSDExecutionEventHandler import UmlSDExecutionEventHandler
from umlshapes.sd.eventhandlers.UmlSDMessageEventHandler import UmlSDMessageEventHandler
from umlshapes.sd.eventhandlers.UmlSdInstanceEventHandler import UmlSdInstanceEventHandler

from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine

from umlio.IOTypes import UmlActors
from umlio.IOTypes import UmlClasses
from umlio.IOTypes import UmlLinks
from umlio.IOTypes import UmlNotes
from umlio.IOTypes import UmlTexts
from umlio.IOTypes import UmlUseCases
from umlio.IOTypes import UmlDocument
from umlio.IOTypes import UmlDocumentTitle
from umlio.IOTypes import UmlDocumentType
from umlio.IOTypes import UmlDocuments
from umlio.IOTypes import UmlLollipopInterfaces
from umlio.IOTypes import UmlSDCombinedFragments
from umlio.IOTypes import UmlSDExecutions
from umlio.IOTypes import UmlSDInstances
from umlio.IOTypes import UmlSDMessages

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

        # doing any effect should be an application preference
        # self.SetEffect(effect=SHOW_EFFECT_SLIDE_TO_RIGHT)               # TODO:  Should be an application preference
        # self.SetEffectTimeout(timeout=200)                              # TODO:  Should be an application preference

        self._createPages()

        self.SetSelection(0)

    @property
    def umlDocuments(self) -> UmlDocuments:
        """
        The input document at UI creation may be out of date.  So recreate it by
        re-reading the shapes from the frames;  Update the internal variable and
        return it

        Returns:  The updated UML Documents

        """
        umlDocuments: UmlDocuments = UmlDocuments({})
        pageCount: int = self.GetPageCount()

        for pageIdx in range(0, pageCount):

            umlDocument:  UmlDocument = UmlDocument()
            page:         Window      = self.GetPage(pageIdx)
            currentTitle: str         = self.GetPageText(pageIdx)

            if isinstance(page, ClassDiagramFrame):
                classDiagramFrame: ClassDiagramFrame = page
                umlDocument.documentType = UmlDocumentType.CLASS_DOCUMENT
                umlDocument = self._toBasicUmlDocument(umlDocument=umlDocument, documentTitle=currentTitle, diagramFrame=classDiagramFrame)
            elif isinstance(page, UseCaseDiagramFrame):
                useCaseDiagramFrame: UseCaseDiagramFrame = page
                umlDocument.documentType = UmlDocumentType.USE_CASE_DOCUMENT
                umlDocument = self._toBasicUmlDocument(umlDocument=umlDocument, documentTitle=currentTitle, diagramFrame=useCaseDiagramFrame)
                self.logger.warning('Not yet implemented')
            elif isinstance(page, SequenceDiagramFrame):
                sequenceDiagramFrame: SequenceDiagramFrame = page
                umlDocument.documentType = UmlDocumentType.SEQUENCE_DOCUMENT
                umlDocument = self._toBasicUmlDocument(umlDocument=umlDocument, documentTitle=currentTitle, diagramFrame=sequenceDiagramFrame)
            else:
                assert False, 'No such frame type'

            umlDocument = self._populateUmlDocument(page=page, umlDocument=umlDocument)
            umlDocuments[umlDocument.documentTitle] = umlDocument

        self._umlDocuments = umlDocuments
        return self._umlDocuments

    def setPage(self, umlDocumentTitle: UmlDocumentTitle):
        self.SetSelection(self._diagramTitleToPage[umlDocumentTitle])

    def _createPages(self):

        for umlDocumentTitle, umlDocument in self._umlDocuments.items():

            documentType: UmlDocumentType = umlDocument.documentType

            if documentType == UmlDocumentType.CLASS_DOCUMENT:
                diagramFrame = ClassDiagramFrame(
                    parent=self,
                    umlPubSubEngine=self._umlPubSubEngine
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

    def _layoutShapes(self, diagramFrame: ClassDiagramFrame | UseCaseDiagramFrame | SequenceDiagramFrame, umlDocument: UmlDocument):

        if isinstance(diagramFrame, ClassDiagramFrame):
            self._layoutClasses(diagramFrame, umlDocument.umlClasses)
            self._layoutNotes(diagramFrame, umlDocument.umlNotes)
            self._layoutTexts(diagramFrame, umlDocument.umlTexts)
            self._layoutLinks(diagramFrame, umlDocument.umlLinks)
            self._layoutLollipops(diagramFrame, umlDocument.umlLollipopInterfaces)
        elif isinstance(diagramFrame, UseCaseDiagramFrame):
            self._layoutActors(diagramFrame, umlDocument.umlActors)
            self._layoutUseCases(diagramFrame, umlDocument.umlUseCases)
            self._layoutNotes(diagramFrame, umlDocument.umlNotes)
            self._layoutTexts(diagramFrame, umlDocument.umlTexts)
            self._layoutLinks(diagramFrame, umlDocument.umlLinks)
        elif isinstance(diagramFrame, SequenceDiagramFrame):
            self._layoutSDInstances(diagramFrame, umlDocument.umlSDInstances)
            self._layoutSDMessages(diagramFrame, umlDocument.umlSDMessages)
            self._layoutSDExecutions(diagramFrame, umlDocument.umlSDExecutions)
            self._layoutSDCombinedFragments(diagramFrame, umlDocument.umlSDCombinedFragments)
            self._layoutNotes(diagramFrame, umlDocument.umlNotes)
            self._layoutTexts(diagramFrame, umlDocument.umlTexts)

    def _layoutClasses(self, diagramFrame: ClassDiagramFrame, umlClasses: UmlClasses):
        for umlClass in umlClasses:
            self._layoutShape(
                umlShape=umlClass,
                diagramFrame=diagramFrame,
                eventHandlerClass=UmlClassEventHandler
            )

    def _layoutNotes(self, diagramFrame: ClassDiagramFrame | UseCaseDiagramFrame | SequenceDiagramFrame, umlNotes: UmlNotes):

        for umlNote in umlNotes:
            self._layoutShape(
                umlShape=umlNote,
                diagramFrame=diagramFrame,
                eventHandlerClass=UmlNoteEventHandler
            )

    def _layoutTexts(self, diagramFrame: ClassDiagramFrame | UseCaseDiagramFrame | SequenceDiagramFrame, umlTexts: UmlTexts):

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

    def _layoutLollipops(self, diagramFrame: ClassDiagramFrame, umlLollipops: UmlLollipopInterfaces):
        for umlLollipop in umlLollipops:
            umlLollipopInterface: UmlLollipopInterface = cast(UmlLollipopInterface, umlLollipop)
            self.logger.info(f'{umlLollipopInterface}')

            diagramFrame.umlDiagram.AddShape(umlLollipopInterface)
            umlLollipopInterface.Show(True)

            lollipopEventHandler: UmlLollipopInterfaceEventHandler = UmlLollipopInterfaceEventHandler(lollipopInterface=umlLollipopInterface)
            lollipopEventHandler.umlPubSubEngine = self._umlPubSubEngine

            umlLollipopInterface.SetEventHandler(lollipopEventHandler)

    def _layoutSDInstances(self, diagramFrame: SequenceDiagramFrame, umlSDInstances: UmlSDInstances):
        dc: ClientDC = ClientDC(diagramFrame)
        diagramFrame.PrepareDC(dc)

        for umlSDInstance in umlSDInstances:
            savedPosition: UmlPosition = umlSDInstance.position
            umlSDInstance.umlFrame = diagramFrame
            diagramFrame.umlDiagram.AddShape(umlSDInstance)
            umlSDInstance.Show(True)

            centerX: int
            centerY: int
            centerX, centerY = umlSDInstance.computeCenterXY(position=savedPosition)
            umlSDInstance.Move(dc, centerX, centerY)

            eventHandler: UmlSdInstanceEventHandler = UmlSdInstanceEventHandler(
                umlSdInstance=umlSDInstance,
                previousEventHandler=umlSDInstance.GetEventHandler()
            )
            eventHandler.umlPubSubEngine = self._umlPubSubEngine
            umlSDInstance.SetEventHandler(eventHandler)

    def _layoutSDMessages(self, diagramFrame: SequenceDiagramFrame, umlSDMessages: UmlSDMessages):
        for umlSDMessage in umlSDMessages:
            umlSDMessage.umlFrame = diagramFrame
            diagramFrame.umlDiagram.AddShape(umlSDMessage)
            umlSDMessage.Show(True)
            umlSDMessage.updateMessage()

            eventHandler: UmlSDMessageEventHandler = UmlSDMessageEventHandler(
                umlSDMessage=umlSDMessage,
                previousEventHandler=umlSDMessage.GetEventHandler()
            )
            eventHandler.umlPubSubEngine = self._umlPubSubEngine
            umlSDMessage.SetEventHandler(eventHandler)

    def _layoutSDExecutions(self, diagramFrame: SequenceDiagramFrame, umlSDExecutions: UmlSDExecutions):
        for umlSDExecution in umlSDExecutions:
            if umlSDExecution.lifeLine is not None:
                umlSDExecution.lifeLine.addExecution(execution=umlSDExecution)
            else:
                diagramFrame.umlDiagram.AddShape(umlSDExecution)
                umlSDExecution.Show(True)

            eventHandler: UmlSDExecutionEventHandler = UmlSDExecutionEventHandler(
                umlSDExecution=umlSDExecution,
                previousEventHandler=umlSDExecution.GetEventHandler()
            )
            eventHandler.umlPubSubEngine = self._umlPubSubEngine
            umlSDExecution.SetEventHandler(eventHandler)

    def _layoutSDCombinedFragments(self, diagramFrame: SequenceDiagramFrame, umlSDCombinedFragments: UmlSDCombinedFragments):
        for umlSDCombinedFragment in umlSDCombinedFragments:
            umlSDCombinedFragment.umlFrame = diagramFrame
            diagramFrame.umlDiagram.AddShape(umlSDCombinedFragment)
            umlSDCombinedFragment.Show(True)

            eventHandler: UmlSDCombinedFragmentEventHandler = UmlSDCombinedFragmentEventHandler(
                umlSDCombinedFragment=umlSDCombinedFragment,
                previousEventHandler=umlSDCombinedFragment.GetEventHandler()
            )
            eventHandler.umlPubSubEngine = self._umlPubSubEngine
            umlSDCombinedFragment.SetEventHandler(eventHandler)

    def _layoutLinks(self, diagramFrame: ClassDiagramFrame | UseCaseDiagramFrame, umlLinks: UmlLinks):
        """
        In all instances you still have to do the addLink call between the shapes.  The
        method respects the end positions and control points that may have been set by the
        deserializer

        Args:
            diagramFrame:
            umlLinks:
        """
        for umlLink in umlLinks:
            umlLink.umlFrame = diagramFrame
            if isinstance(umlLink, UmlInheritance):
                umInheritance: UmlInheritance = umlLink
                subClass  = umInheritance.subClass
                baseClass = umInheritance.baseClass

                subClass.addLink(umlLink=umInheritance, destinationClass=baseClass)

                diagramFrame.umlDiagram.AddShape(umInheritance)
                umInheritance.Show(True)

                umlLinkEventHandler: UmlLinkEventHandler = UmlLinkEventHandler(umlLink=umlLink, previousEventHandler=umlLink.GetEventHandler())
                umlLinkEventHandler.umlPubSubEngine = self._umlPubSubEngine
                umlLink.SetEventHandler(umlLinkEventHandler)

            elif isinstance(umlLink, UmlNoteLink):
                umlNoteLink:      UmlNoteLink = umlLink
                sourceNote:       UmlNote     = umlNoteLink.sourceNote
                destinationClass: UmlClass    = umlNoteLink.destinationClass

                sourceNote.addLink(umlNoteLink=umlNoteLink, umlClass=destinationClass)

                diagramFrame.umlDiagram.AddShape(umlNoteLink)
                umlNoteLink.Show(True)
                eventHandler: UmlNoteLinkEventHandler = UmlNoteLinkEventHandler(umlNoteLink=umlNoteLink, previousEventHandler=umlNoteLink.GetEventHandler())
                eventHandler.umlPubSubEngine = self._umlPubSubEngine
                umlNoteLink.SetEventHandler(eventHandler)

            elif isinstance(umlLink, (UmlAssociation, UmlComposition, UmlAggregation)):

                source = umlLink.sourceShape
                dest   = umlLink.destinationShape
                source.addLink(umlLink, dest)  # type: ignore

                diagramFrame.umlDiagram.AddShape(umlLink)
                umlLink.Show(True)
                # noinspection PyUnusedLocal
                umlAssociationEventHandler: UmlAssociationEventHandler = UmlAssociationEventHandler(umlAssociation=umlLink, umlPubSubEngine=self._umlPubSubEngine)

            elif isinstance(umlLink, UmlInterface):
                umlInterface: UmlInterface = umlLink
                interfaceClass:    UmlClass = umlInterface.interfaceClass
                implementingClass: UmlClass = umlInterface.implementingClass

                implementingClass.addLink(umlLink=umlInterface, destinationClass=interfaceClass)
                diagramFrame.umlDiagram.AddShape(umlInterface)
                umlInterface.Show(True)

                umlLinkEventHandler = UmlLinkEventHandler(umlLink=umlInterface, previousEventHandler=umlInterface.GetEventHandler())
                umlLinkEventHandler.umlPubSubEngine = self._umlPubSubEngine
                umlLink.SetEventHandler(umlLinkEventHandler)

    def _layoutShape(self, umlShape: UmlShape, diagramFrame: ClassDiagramFrame | UseCaseDiagramFrame | SequenceDiagramFrame, eventHandlerClass: type[UmlBaseEventHandler]):
        """

        Args:
            umlShape:
            diagramFrame:
            eventHandlerClass:
        """

        umlShape.umlFrame = diagramFrame
        diagram: UmlDiagram = diagramFrame.umlDiagram

        eventHandler: UmlBaseEventHandler = eventHandlerClass(previousEventHandler=umlShape.GetEventHandler())
        eventHandler.SetShape(umlShape)
        eventHandler.umlPubSubEngine = self._umlPubSubEngine

        eventHandler.SetPreviousHandler(umlShape.GetEventHandler())
        umlShape.SetEventHandler(eventHandler)

        diagram.AddShape(umlShape)
        umlShape.Show(True)

        diagramFrame.refresh()

    def _toBasicUmlDocument(self, umlDocument: UmlDocument, documentTitle: str, diagramFrame: DiagramFrame) -> UmlDocument:
        """
        Document type set by caller
        Args:
            umlDocument:    Partial UML Document
            documentTitle:  The string from the tab (Not visible but maintained)
            diagramFrame:   The associated diagram frame

        Returns:  The updated UML Document (additional meta data)
        """
        scrollPosX, scrollPosY = diagramFrame.GetViewStart()

        xUnit, yUnit = diagramFrame.GetScrollPixelsPerUnit()

        umlDocument.documentTitle   = UmlDocumentTitle(documentTitle)
        umlDocument.scrollPositionX = scrollPosX
        umlDocument.scrollPositionY = scrollPosY
        umlDocument.pixelsPerUnitX  = xUnit
        umlDocument.pixelsPerUnitY  = yUnit

        return umlDocument

    def _populateUmlDocument(self, page: Window, umlDocument: UmlDocument) -> UmlDocument:

        umlFrame: UmlFrame = cast(UmlFrame, page)

        umlShapes: UmlShapes = umlFrame.umlShapes

        for umlShape in umlShapes:
            # noinspection PyUnusedLocal
            match umlShape:
                case UmlClass() as umlShape:
                    umlDocument.umlClasses.append(umlShape)
                case UmlInheritance() | UmlInterface() | UmlAssociation() | UmlNoteLink() as umlShape:
                    umlDocument.umlLinks.append(umlShape)
                case UmlLollipopInterface() as umlShape:
                    umlDocument.umlLinks.append(cast(UmlLink, umlShape))  # temp cast until umlio supports UmlLollipopInterfaces
                case UmlNote() as umlShape:
                    umlDocument.umlNotes.append(umlShape)
                case UmlText() as umlShape:
                    umlDocument.umlTexts.append(umlShape)
                case UmlUseCase() as umlShape:
                    umlDocument.umlUseCases.append(umlShape)
                case UmlActor() as umlShape:
                    umlDocument.umlActors.append(umlShape)
                case UmlSDInstance() as umlShape:
                    umlDocument.umlSDInstances.append(umlShape)
                case UmlSDMessage() as umlShape:
                    umlDocument.umlSDMessages.append(umlShape)
                case UmlSDExecution() as umlShape:
                    umlDocument.umlSDExecutions.append(umlShape)
                case UmlSDCombinedFragment() as umlShape:
                    umlDocument.umlSDCombinedFragments.append(umlShape)
                case UmlControlPoint() as umlShape:
                    pass
                case _:
                    self.logger.warning(f'Unknown Uml object type: {umlShape}, not saved')

        return umlDocument
