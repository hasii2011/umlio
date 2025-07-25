
from logging import Logger
from logging import getLogger

from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine
from wx import SplitterWindow
from wx import Window


from tests.demo.DiagramManager import DiagramManager
from tests.demo.ProjectTree import ProjectTree
from tests.demo.ProjectTree import TreeData
from tests.demo.ProjectTree import TreeNodeIDs
from tests.demo.eventengine.DemoAppPubSubEngine import DemoAppPubSubEngine
from tests.demo.eventengine.DemoMessageType import DemoMessageType
from tests.demo.eventengine.IAppPubSubEngine import UniqueId

from umlio.IOTypes import UmlProject


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
                                          callback=self._onDiagramSelectionChanged)

    def _onDiagramSelectionChanged(self, treeData: TreeData):
        self.logger.debug(f'{treeData=}')
        self._diagramManager.setPage(treeData.documentName)
