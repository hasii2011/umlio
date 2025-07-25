
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import EVT_TREE_SEL_CHANGED
from wx import TR_HAS_BUTTONS

from wx import TreeCtrl
from wx import TreeEvent
from wx import TreeItemId
from wx import Window

from tests.demo.eventengine.DemoMessageType import DemoMessageType
from tests.demo.eventengine.IAppPubSubEngine import IAppPubSubEngine
from tests.demo.eventengine.IAppPubSubEngine import UniqueId

from umlshapes.UmlUtils import UmlUtils

from umlio.IOTypes import UmlDocumentTitle
from umlio.IOTypes import UmlProject


TreeNodeID = NewType('TreeNodeID', str)


@dataclass
class TreeData:
    documentName: UmlDocumentTitle
    treeNodeID:   TreeNodeID        # The underlying TreeItemId (ID) is opaque


TreeNodeIDs = NewType('TreeNodeIDs', List[TreeNodeID])


class ProjectTree(TreeCtrl):
    def __init__(self, parent: Window, umlProject: UmlProject, appEventEngine: IAppPubSubEngine):

        self.logger: Logger = getLogger(__name__)

        super().__init__(parent=parent, style=TR_HAS_BUTTONS)

        self._umlProject:     UmlProject      = umlProject
        self._appEventEngine: IAppPubSubEngine = appEventEngine
        self._treeNodeIDs:    TreeNodeIDs     = TreeNodeIDs([])

        self.root: TreeItemId = self.AddRoot(umlProject.fileName.stem)

        self._createDocumentNodes()

        self.Expand(self.root)

        self.SelectItem(self.GetFirstChild(self.root)[0])

        self.Bind(EVT_TREE_SEL_CHANGED, self._onDiagramSelectionChanged)

    @property
    def treeNodeIDs(self) -> TreeNodeIDs:
        return self._treeNodeIDs

    def _createDocumentNodes(self):

        for documentName in self._umlProject.umlDocuments.keys():
            documentNode: TreeItemId = self.AppendItem(self.root, documentName)

            treeNodeID: TreeNodeID = TreeNodeID(UmlUtils.getID())
            treeData:   TreeData   = TreeData(
                documentName=documentName,
                treeNodeID=treeNodeID
            )
            self._treeNodeIDs.append(treeNodeID)

            self.SetItemData(item=documentNode, data=treeData)

    def _onDiagramSelectionChanged(self, treeEvent: TreeEvent):

        item: TreeItemId = treeEvent.GetItem()

        treeData: TreeData = self.GetItemData(item)

        self.logger.debug(f'{treeData=}')

        self._appEventEngine.sendMessage(DemoMessageType.DIAGRAM_SELECTION_CHANGED,
                                         uniqueId=UniqueId(treeData.treeNodeID),
                                         treeData=treeData)
