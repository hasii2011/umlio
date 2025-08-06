
from typing import NewType

from wx import NewIdRef as wxNewIdRef

ID_REFERENCE = NewType('ID_REFERENCE', int)


INITIAL_X:   int = 100
INITIAL_Y:   int = 100

INCREMENT_X: int = 25
INCREMENT_Y: int = 25


class Identifiers:
    ID_OPEN_XML_FILE:     ID_REFERENCE = wxNewIdRef()
    ID_OPEN_PROJECT_FILE: ID_REFERENCE = wxNewIdRef()
