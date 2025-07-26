
from logging import Logger
from logging import getLogger
from pathlib import Path
from typing import List
from typing import cast

from wx import CallAfter
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_OPEN
from wx import FRAME_FLOAT_ON_PARENT
from wx import FileSelector
from wx import ID_EXIT

from wx import Menu
from wx import MenuBar
from wx import NB_LEFT
from wx import Notebook
from wx.core import CallLater

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from umlshapes.preferences.UmlPreferences import UmlPreferences

from umlshapes.pubsubengine.UmlPubSubEngine import UmlPubSubEngine

from tests.demo.eventengine.DemoAppPubSubEngine import DemoAppPubSubEngine

from umlio.IOTypes import UmlProject
from umlio.Reader import Reader

from tests.demo.DemoCommon import Identifiers
from tests.demo.ProjectPanel import ProjectPanel

FRAME_WIDTH:  int = 800
FRAME_HEIGHT: int = 400


class DemoAppFrame(SizedFrame):
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        super().__init__(parent=None, title='Demonstrate UMLIO', size=(FRAME_WIDTH, FRAME_HEIGHT), style=DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerProps(expand=True, proportion=1)

        self._notebook: Notebook = cast(Notebook, None)

        self._openProjects:    List[UmlProject] = []
        self._demoEventEngine: DemoAppPubSubEngine  = DemoAppPubSubEngine()
        self._umlPubSubEngine: UmlPubSubEngine  = UmlPubSubEngine()

        self._createApplicationMenuBar()

        self.CreateStatusBar()  # should always do this when there's a resize border
        self.SetAutoLayout(True)

        self.Show(True)

        self._preferences: UmlPreferences = UmlPreferences()

        self._pyutInterfaceCount: int = 0

    def _createApplicationMenuBar(self):

        menuBar:  MenuBar = MenuBar()
        fileMenu: Menu    = Menu()

        fileMenu.Append(Identifiers.ID_OPEN_XML_FILE, 'Load Xml Diagram')
        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, '&Quit', "Quit Application")
        fileMenu.AppendSeparator()
        # fileMenu.Append(ID_PREFERENCES, "P&references", "Uml preferences")

        menuBar.Append(fileMenu, 'File')

        self.SetMenuBar(menuBar)

        # self.Bind(EVT_MENU, self._onOglPreferences, id=ID_PREFERENCES)
        self.Bind(EVT_MENU, self._onLoadXmlFile, id=Identifiers.ID_OPEN_XML_FILE)

    # def _onDisplayElement(self, event: CommandEvent):
    #
    #     menuId:              int                 = event.GetId()
    #     shapeCreator:        ShapeCreator        = self._shapeCreator
    #     relationshipCreator: RelationshipCreator = self._relationshipCreator
    #
    #     # noinspection PyUnreachableCode
    #     match menuId:
    #         case Identifiers.ID_DISPLAY_UML_CLASS:
    #             shapeCreator.displayShape(Identifiers.ID_DISPLAY_UML_CLASS)
    #             self.SetStatusText('See the shape !!')
    #         case Identifiers.ID_DISPLAY_UML_TEXT:
    #             shapeCreator.displayShape(Identifiers.ID_DISPLAY_UML_TEXT)
    #         case Identifiers.ID_DISPLAY_UML_NOTE:
    #             shapeCreator.displayShape(Identifiers.ID_DISPLAY_UML_NOTE)
    #         case Identifiers.ID_DISPLAY_UML_USE_CASE:
    #             shapeCreator.displayShape(Identifiers.ID_DISPLAY_UML_USE_CASE)
    #         case Identifiers.ID_DISPLAY_UML_ACTOR:
    #             shapeCreator.displayShape(Identifiers.ID_DISPLAY_UML_ACTOR)
    #
    #         case Identifiers.ID_DISPLAY_UML_ASSOCIATION:
    #             relationshipCreator.displayRelationship(idReference=Identifiers.ID_DISPLAY_UML_ASSOCIATION)
    #         case Identifiers.ID_DISPLAY_UML_COMPOSITION:
    #             relationshipCreator.displayRelationship(idReference=Identifiers.ID_DISPLAY_UML_COMPOSITION)
    #         case Identifiers.ID_DISPLAY_UML_AGGREGATION:
    #             relationshipCreator.displayRelationship(idReference=Identifiers.ID_DISPLAY_UML_AGGREGATION)
    #
    #         case Identifiers.ID_DISPLAY_UML_INHERITANCE:
    #             relationshipCreator.displayRelationship(idReference=Identifiers.ID_DISPLAY_UML_INHERITANCE)
    #         case Identifiers.ID_DISPLAY_UML_INTERFACE:
    #             relationshipCreator.displayRelationship(idReference=Identifiers.ID_DISPLAY_UML_INTERFACE)
    #         # case self._ID_DISPLAY_SEQUENCE_DIAGRAM:
    #         #     self._displaySequenceDiagram()

    # noinspection PyUnusedLocal
    def _onLoadXmlFile(self, event: CommandEvent):

        wildcard: str = (
            f'Extended Markup Language '
            f' (*, xml '
            f'|*.xml'
        )

        selectedFile: str = FileSelector("Choose a XML file to load", wildcard=wildcard, flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR)

        if selectedFile != '':
            self._loadXmlFile(Path(selectedFile))

    def _loadXmlFile(self, fileName: Path):

        reader: Reader = Reader()

        umlProject: UmlProject = reader.readXmlFile(fileName=fileName)

        self.logger.debug(f'{umlProject=}')
        # self._eventEngine.sendEvent(eventType=EventType.LoadOglProject, oglProject=oglProject)

        self._loadNewProject(umlProject)

    def _loadNewProject(self, umlProject: UmlProject):

        if self._notebook is None:
            self._createTheOverArchingNotebook()

        projectPanel: ProjectPanel = ProjectPanel(self._notebook,
                                                  appEventEngine=self._demoEventEngine,
                                                  umlPubSibEngine=self._umlPubSubEngine,
                                                  umlProject=umlProject)
        self._notebook.AddPage(page=projectPanel, text=umlProject.fileName.stem)
        self._openProjects.append(umlProject)

    def _createTheOverArchingNotebook(self):
        """
        Lazy UI creation
        """
        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerProps(expand=True, proportion=1)
        sizedPanel.SetSizerType('vertical')

        self._notebook = Notebook(sizedPanel, style=NB_LEFT)    # TODO: should be an application preference
        self._notebook.SetSizerProps(expand=True, proportion=1)
        CallLater(millis=200, callableObj=self._notebook.PostSizeEventToParent)

    # noinspection PyUnusedLocal
    def onPageClosing(self, event):
        """
        Event handler that is called when a page in the notebook is closing
        """
        page = self._notebook.GetCurrentPage()
        page.Close()
        if len(self._openProjects) == 0:
            CallAfter(self._notebook.Destroy)
            self._notebook = None

    # def _createLollipopInterface(self, requestingUmlClass: UmlClass, perimeterPoint: UmlPosition):
    #     """
    #
    #     Args:
    #         requestingUmlClass:
    #         perimeterPoint:
    #     """
    #
    #     interfaceName: str = f'{self._preferences.defaultNameInterface}{self._pyutInterfaceCount}'
    #     self._pyutInterfaceCount += 1
    #
    #     pyutInterface:        PyutInterface        = PyutInterface(interfaceName)
    #     pyutInterface.addImplementor(ClassName(requestingUmlClass.pyutClass.name))
    #
    #     umlLollipopInterface: UmlLollipopInterface = UmlLollipopInterface(pyutInterface=pyutInterface)
    #     umlLollipopInterface.attachedTo            = requestingUmlClass
    #
    #     attachmentSide: AttachmentSide      = UmlUtils.attachmentSide(x=perimeterPoint.x, y=perimeterPoint.y, rectangle=requestingUmlClass.rectangle)
    #     umlLollipopInterface.attachmentSide = attachmentSide
    #     umlLollipopInterface.lineCentum     = UmlUtils.computeLineCentum(attachmentSide=attachmentSide, umlPosition=perimeterPoint, rectangle=requestingUmlClass.rectangle)
    #
    #     self.logger.debug(f'{umlLollipopInterface.attachmentSide=} {umlLollipopInterface.lineCentum=}')
    #
    #     umlLollipopInterface.SetCanvas(self)
    #     diagram: UmlDiagram = self._diagramFrame.umlDiagram
    #
    #     diagram.AddShape(umlLollipopInterface)
    #     umlLollipopInterface.Show(show=True)
    #     self.logger.info(f'UmlInterface added: {umlLollipopInterface}')
    #
    #     eventHandler: UmlLollipopInterfaceEventHandler = UmlLollipopInterfaceEventHandler(lollipopInterface=umlLollipopInterface)
    #     eventHandler.SetPreviousHandler(umlLollipopInterface.GetEventHandler())
    #     umlLollipopInterface.SetEventHandler(eventHandler)
    #
    #     umlFrame:       UmlClassDiagramFrame = self._diagramFrame
    #     eventEngine:    UmlEventEngine       = umlFrame.eventEngine
    #     pyutInterfaces: PyutInterfaces       = eventHandler.getDefinedInterfaces()
    #
    #     with DlgEditInterface(parent=umlFrame, oglInterface2=umlLollipopInterface, eventEngine=eventEngine, pyutInterfaces=pyutInterfaces) as dlg:
    #         if dlg.ShowModal() == OK:
    #             umlFrame.refresh()
