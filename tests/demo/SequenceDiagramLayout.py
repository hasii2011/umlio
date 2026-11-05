
from logging import Logger
from logging import getLogger
from typing import Optional

from wx import ClientDC

from umlshapes.frames.SequenceDiagramFrame import SequenceDiagramFrame

from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine

from umlshapes.types.UmlPosition import UmlPosition

from umlshapes.sd.UmlSDLifeLine import UmlSDLifeLine

from umlshapes.sd.eventhandlers.UmlSDMessageEventHandler import UmlSDMessageEventHandler
from umlshapes.sd.eventhandlers.UmlSdInstanceEventHandler import UmlSdInstanceEventHandler
from umlshapes.sd.eventhandlers.UmlSDExecutionEventHandler import UmlSDExecutionEventHandler
from umlshapes.sd.eventhandlers.UmlSDCombinedFragmentEventHandler import UmlSDCombinedFragmentEventHandler

from umlio.IOTypes import UmlDocument
from umlio.IOTypes import UmlSDMessages
from umlio.IOTypes import UmlSDInstances
from umlio.IOTypes import UmlSDExecutions
from umlio.IOTypes import UmlSDCombinedFragments


class SequenceDiagramLayout:
    """
    Handles layout and event handler binding for Sequence Diagram shapes on canvas.
    """

    def __init__(self, umlPubSubEngine: UmlPubSubEngine):
        """
        Args:
            umlPubSubEngine: The pub-sub event engine for diagram interactions
        """
        self.logger:           Logger          = getLogger(__name__)
        self._umlPubSubEngine: UmlPubSubEngine = umlPubSubEngine

    def layout(self, diagramFrame: SequenceDiagramFrame, umlDocument: UmlDocument):
        """
        Positions and registers all sequence diagram elements on the canvas.

        Args:
            diagramFrame: The SequenceDiagramFrame canvas
            umlDocument:  The UmlDocument holding SD instances, messages, executions, and fragments
        """
        self.layoutSDInstances(diagramFrame=diagramFrame, umlSDInstances=umlDocument.umlSDInstances)
        self.layoutSDMessages(diagramFrame=diagramFrame, umlSDMessages=umlDocument.umlSDMessages)
        self.layoutSDExecutions(umlSDExecutions=umlDocument.umlSDExecutions)
        self.layoutSDCombinedFragments(diagramFrame=diagramFrame, umlSDCombinedFragments=umlDocument.umlSDCombinedFragments)

    def layoutSDInstances(self, diagramFrame: SequenceDiagramFrame, umlSDInstances: UmlSDInstances):
        """
        Positions participant instances on the canvas and attaches event handlers.

        Args:
            diagramFrame:   The SequenceDiagramFrame canvas
            umlSDInstances: The collection of UmlSDInstance objects to layout
        """
        dc: ClientDC = ClientDC(diagramFrame)
        diagramFrame.PrepareDC(dc)

        for umlSDInstance in umlSDInstances:

            savedPosition: UmlPosition = umlSDInstance.position
            umlSDInstance.umlFrame = diagramFrame
            diagramFrame.umlDiagram.AddShape(umlSDInstance)
            umlSDInstance.Show(True)

            totalHeight: int = int(umlSDInstance.GetHeight())
            totalWidth:  int = int(umlSDInstance.GetWidth())
            centerX:     int = savedPosition.x + (totalWidth // 2)
            centerY:     int = savedPosition.y + (totalHeight // 2)
            umlSDInstance.Move(dc, centerX, centerY)

            eventHandler: UmlSdInstanceEventHandler = UmlSdInstanceEventHandler(
                umlSdInstance=umlSDInstance,
                previousEventHandler=umlSDInstance.GetEventHandler()
            )
            eventHandler.umlPubSubEngine = self._umlPubSubEngine
            umlSDInstance.SetEventHandler(eventHandler)

    def layoutSDMessages(self, diagramFrame: SequenceDiagramFrame, umlSDMessages: UmlSDMessages):
        """
        Positions messages between lifelines on canvas and attaches event handlers.

        Args:
            diagramFrame:  The SequenceDiagramFrame canvas
            umlSDMessages: The collection of UmlSDMessage objects to layout
        """
        dc: ClientDC = ClientDC(diagramFrame)
        diagramFrame.PrepareDC(dc)

        for umlSDMessage in umlSDMessages:

            umlSDMessage.umlFrame = diagramFrame
            diagramFrame.umlDiagram.AddShape(umlSDMessage)
            umlSDMessage.Show(True)

            sourceLifeLine: Optional[UmlSDLifeLine] = umlSDMessage.GetFrom()
            destLifeLine:   Optional[UmlSDLifeLine] = umlSDMessage.GetTo()

            if sourceLifeLine is not None:
                sourceLifeLine.addMessage(umlSDMessage=umlSDMessage, destinationLifeLine=destLifeLine)
            else:
                if destLifeLine is not None:
                    destLifeLine.addMessage(umlSDMessage=umlSDMessage)

            umlSDMessage.fromY = umlSDMessage.fromY
            umlSDMessage.toY   = umlSDMessage.toY
            umlSDMessage.updateMessage()
            umlSDMessage.OnMoveLink(dc=dc)

            eventHandler: UmlSDMessageEventHandler = UmlSDMessageEventHandler(
                umlSDMessage=umlSDMessage,
                previousEventHandler=umlSDMessage.GetEventHandler()
            )
            eventHandler.umlPubSubEngine = self._umlPubSubEngine
            umlSDMessage.SetEventHandler(eventHandler)

    def layoutSDExecutions(self, umlSDExecutions: UmlSDExecutions):
        """
        Attaches execution bars to their respective lifelines.

        Args:
            umlSDExecutions: The collection of UmlSDExecution objects to layout
        """
        for umlSDExecution in umlSDExecutions:

            umlSDExecution.lifeLine.addExecution(execution=umlSDExecution)

            eventHandler: UmlSDExecutionEventHandler = UmlSDExecutionEventHandler(
                umlSDExecution=umlSDExecution,
                previousEventHandler=umlSDExecution.GetEventHandler()
            )
            eventHandler.umlPubSubEngine = self._umlPubSubEngine
            umlSDExecution.SetEventHandler(eventHandler)

    def layoutSDCombinedFragments(self, diagramFrame: SequenceDiagramFrame, umlSDCombinedFragments: UmlSDCombinedFragments):
        """
        Adds combined fragments to the canvas and attaches event handlers.

        Args:
            diagramFrame:           The SequenceDiagramFrame canvas
            umlSDCombinedFragments: The collection of UmlSDCombinedFragment objects to layout
        """
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
