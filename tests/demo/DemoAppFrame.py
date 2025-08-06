
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

from tests.demo.pubsubengine.DemoAppPubSubEngine import DemoAppPubSubEngine

from umlio.IOTypes import UmlProject
from umlio.IOTypes import XML_SUFFIX
from umlio.IOTypes import PROJECT_SUFFIX

from umlio.Reader import Reader

from tests.demo.DemoCommon import Identifiers
from tests.demo.ProjectPanel import ProjectPanel

FRAME_WIDTH:  int = 800
FRAME_HEIGHT: int = 400

PROJECT_WILDCARD: str = f'UML Diagrammer files (*.{PROJECT_SUFFIX})|*{PROJECT_SUFFIX}'
XML_WILDCARD:     str = f'Extensible Markup Language (*.{XML_SUFFIX})|*{XML_SUFFIX}'


class DemoAppFrame(SizedFrame):
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        super().__init__(parent=None, title='Demonstrate UMLIO', size=(FRAME_WIDTH, FRAME_HEIGHT), style=DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerProps(expand=True, proportion=1)

        self._notebook: Notebook = cast(Notebook, None)

        self._openProjects:        List[UmlProject]     = []
        self._demoAppPubSubEngine: DemoAppPubSubEngine  = DemoAppPubSubEngine()
        self._umlPubSubEngine:     UmlPubSubEngine      = UmlPubSubEngine()

        self._createApplicationMenuBar()

        self.CreateStatusBar()  # should always do this when there's a resize border
        self.SetAutoLayout(True)

        self.Show(True)

        self._preferences: UmlPreferences = UmlPreferences()

        self._pyutInterfaceCount: int = 0

    def _createApplicationMenuBar(self):

        menuBar:  MenuBar = MenuBar()
        fileMenu: Menu    = Menu()

        fileMenu.Append(Identifiers.ID_OPEN_PROJECT_FILE, 'Open Project')
        fileMenu.Append(Identifiers.ID_OPEN_XML_FILE,     'Open Xml Diagram')
        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, '&Quit', "Quit Application")
        fileMenu.AppendSeparator()
        # fileMenu.Append(ID_PREFERENCES, "P&references", "Uml preferences")

        menuBar.Append(fileMenu, 'File')

        self.SetMenuBar(menuBar)

        # self.Bind(EVT_MENU, self._onOglPreferences, id=ID_PREFERENCES)
        self.Bind(EVT_MENU, self._onLoadProject, id=Identifiers.ID_OPEN_PROJECT_FILE)
        self.Bind(EVT_MENU, self._onLoadXmlFile, id=Identifiers.ID_OPEN_XML_FILE)

    # noinspection PyUnusedLocal
    def _onLoadProject(self, event: CommandEvent):

        selectedFile: str = FileSelector("Choose a project file to load", wildcard=PROJECT_WILDCARD, flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR)
        if selectedFile != '':
            self._loadProjectFile(Path(selectedFile))

    # noinspection PyUnusedLocal
    def _onLoadXmlFile(self, event: CommandEvent):

        selectedFile: str = FileSelector("Choose a XML file to load", wildcard=XML_WILDCARD, flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR)
        if selectedFile != '':
            self._loadXmlFile(Path(selectedFile))

    def _loadProjectFile(self, fileName: Path):
        reader: Reader = Reader()

        umlProject: UmlProject = reader.readProjectFile(fileName=fileName)
        self._loadNewProject(umlProject)

    def _loadXmlFile(self, fileName: Path):

        reader: Reader = Reader()

        umlProject: UmlProject = reader.readXmlFile(fileName=fileName)

        self.logger.debug(f'{umlProject=}')

        self._loadNewProject(umlProject)

    def _loadNewProject(self, umlProject: UmlProject):

        if self._notebook is None:
            self._createTheOverArchingNotebook()

        projectPanel: ProjectPanel = ProjectPanel(self._notebook,
                                                  appEventEngine=self._demoAppPubSubEngine,
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
