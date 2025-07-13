
from logging import Logger
from logging import getLogger
from pathlib import Path

from umlio.IOTypes import UmlDiagrams
from umlio.IOTypes import UmlProject


class UnTangler:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._umlProject:  UmlProject = UmlProject()
        self._umlDiagrams: UmlDiagrams = UmlDiagrams({})

    def untangleFile(self, fileName: Path):
        pass

    def untangleXml(self, xmlString: str, fileName: Path):
        """
        Untangle the input Xml string to UmlShapes
        Args:
            fileName:  The file name from which the XML came from
            xmlString:   The string with the raw XML
        """
        pass

    @property
    def umlProject(self) -> UmlProject:
        return self._umlProject

    @property
    def umlDiagrams(self) -> UmlDiagrams:
        return self.umlDiagrams
