
from logging import Logger
from logging import getLogger

from wx import EVT_TREE_SEL_CHANGED
from wx import TR_HAS_BUTTONS
from wx import TreeCtrl
from wx import TreeEvent
from wx import TreeItemId
from wx import Window

from umlio.IOTypes import UmlProject


class ProjectTree(TreeCtrl):
    def __init__(self, parent: Window, umlProject: UmlProject):

        self.logger: Logger = getLogger(__name__)
        super().__init__(parent=parent, style=TR_HAS_BUTTONS)

        self._umlProject: UmlProject = umlProject
        self.root = self.AddRoot(umlProject.fileName.stem)

        self.Expand(self.root)

        for diagramName in self._umlProject.umlDiagrams.keys():

            child: TreeItemId = self.AppendItem(self.root, diagramName)
            self.SetItemData(item=child, data=self._umlProject.umlDiagrams[diagramName])

        self.Bind(EVT_TREE_SEL_CHANGED, self._onDiagramSelectionChanged)

    def _onDiagramSelectionChanged(self, event: TreeEvent):

        item: TreeItemId = event.GetItem()
        data = self.GetItemData(item)
        self.logger.info(f'{item=}')
        self.logger.info(f'{data=}')

