
from logging import Logger
from logging import getLogger

from umlshapes.eventengine.UmlEventEngine import UmlEventEngine
from wx import SplitterWindow
from wx import Window

from tests.demo.DiagramManager import DiagramManager
from tests.demo.ProjectTree import ProjectTree
from umlio.IOTypes import UmlProject


class ProjectPanel(SplitterWindow):
    def __init__(self, parent: Window, umlEventEngine: UmlEventEngine, umlProject: UmlProject):
        """

        Args:
            parent:
            umlEventEngine:
            umlProject:
        """

        self.logger: Logger = getLogger(__name__)
        super().__init__(parent=parent)

        projectTree:    ProjectTree    = ProjectTree(parent=self, umlProject=umlProject)
        diagramManager: DiagramManager = DiagramManager(parent=self, umlEventEngine=umlEventEngine, umlDiagrams=umlProject.umlDiagrams)

        self.SetMinimumPaneSize(200)

        self.SplitVertically(projectTree, diagramManager)
