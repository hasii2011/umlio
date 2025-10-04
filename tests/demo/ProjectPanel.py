
from logging import Logger
from logging import getLogger

from wx import Size
from wx import Window
from wx import SplitterWindow

from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine

from umlio.IOTypes import UmlProject

from tests.demo.DiagramManager import DiagramManager
from tests.demo.ProjectTree import ProjectTree
from tests.demo.ProjectTree import TreeData
from tests.demo.ProjectTree import TreeNodeIDs

from tests.demo.pubsubengine.DemoAppPubSubEngine import DemoAppPubSubEngine
from tests.demo.pubsubengine.DemoMessageType import DemoMessageType
from tests.demo.pubsubengine.IAppPubSubEngine import UniqueId


class ProjectPanel(SplitterWindow):
    def __init__(self, parent: Window, appEventEngine: DemoAppPubSubEngine, umlPubSibEngine: UmlPubSubEngine, umlProject: UmlProject):
        """

        Args:
            parent:
            appEventEngine:     The event engin that the demonstration applications uses to communicate within its UI components
            umlPubSibEngine:    The pub sub engine that UML Shapes uses to communicate within itself and the wrapper application
            umlProject:
        """

        self.logger: Logger = getLogger(__name__)
        super().__init__(parent=parent)

        self.appEventEngine: DemoAppPubSubEngine = appEventEngine

        self._projectTree:    ProjectTree    = ProjectTree(parent=self, appEventEngine=appEventEngine, umlProject=umlProject)
        self._diagramManager: DiagramManager = DiagramManager(parent=self, umlPubSubEngine=umlPubSibEngine, umlDocuments=umlProject.umlDocuments)

        self.SetMinimumPaneSize(200)

        self.SplitVertically(self._projectTree, self._diagramManager)

        treeNodeIDs: TreeNodeIDs = self._projectTree.treeNodeIDs
        for treeNodeID in treeNodeIDs:
            self.appEventEngine.subscribe(eventType=DemoMessageType.DIAGRAM_SELECTION_CHANGED,
                                          uniqueId=UniqueId(treeNodeID),
                                          listener=self._diagramSelectionChangedListener)

        windowSize: Size = parent.GetSize()

        sashPosition: int = round(windowSize.width * 0.3)     # TODO:  This should be a preference
        self.logger.info(f'{sashPosition=}')
        self.SetSashPosition(position=sashPosition, redraw=True)

    def _diagramSelectionChangedListener(self, treeData: TreeData):
        self.logger.debug(f'{treeData=}')
        self._diagramManager.setPage(treeData.documentName)
