"""
Type stub for the untangle library (XML to Python objects).

Background & Problem Statement:
--------------------------------
The `umlio` package uses `untangle` to parse and navigate serialized diagram XML structures.
In the untyped `untangle` library, attribute indexing on `Element` is implemented as:

    def __getitem__(self, key):
        return self._attributes.get(key)

Because Python's `dict.get()` returns `None` when a key does not exist, PyCharm's static code
inspection infers the return type of `element[key]` as `Any | None` (or `Optional[Any]`).
When deserializing XML attributes into strictly typed variables or domain models
(e.g., `displayStr: str = classElement[...]` or `sdInstance.id = instanceElement[...]`),
PyCharm flags every single attribute lookup across all deserializers with:

    Expected type 'str', got 'Any | None' instead

Littering production deserializers with dozens of redundant runtime `None` checks
(e.g., `if val is not None:`) adds cognitive noise and boilerplate without runtime benefit,
since the UML diagram XML schemas guarantee the presence of required attributes.

Architectural Solution:
-----------------------
This type stub defines the type contract directly for IDEs and type checkers:
1. `Element.__getitem__(self, key: str) -> Any`: Informs PyCharm that attribute indexing
   returns a defined object rather than `Any | None`, resolving all inspection warnings project-wide.
2. `Element.get_elements(self, name: Optional[str] = None) -> Any`: Returns `Any` so that
   custom collection types (such as `Elements = NewType('Elements', List[Element])`)
   can be assigned directly without incompatible type errors.
3. `Element.__getattr__(self, name: str) -> Any`: Supports dynamic dot-notation child
   element access (e.g., `element.ModelSDInstance`) without triggering unresolved attribute warnings.

PEP 561 Stub Package Integration:
---------------------------------
Python Enhancement Proposal 561 ("Distributing and Packaging Type Information") specifies
how type checkers and IDEs locate type annotations for untyped third-party libraries:

1. Stub-Only Package Naming:
   PEP 561 establishes that stubs for an external library named `<package>` must be placed
   in a directory named `<package>-stubs` (hence `untangle-stubs`).
2. Source Root Discovery:
   Because `src/` is configured as the project's Sources Root, both PyCharm and mypy
   scan `src/` for installed modules and stub packages. When PyCharm encounters
   `src/untangle-stubs/`, the PEP 561 resolver automatically maps it to `import untangle`.
3. Zero-Configuration Advantage:
   Placing stubs in generic directories like `typings/` or `src/umlio/typings/` requires
   either manual IDE directory markings ("Mark as Sources Root") or subpackage prefixing
   (`umlio.typings.untangle`). In contrast, `src/untangle-stubs/` is discovered natively
   out of the box with zero IDE configuration changes or `.iml` modifications.
4. Static Type Checker Behavior:
   Command-line checkers like mypy discover `src/untangle-stubs/` on `MYPYPATH=src`
   and verify type safety across the entire codebase cleanly.
"""

from io import StringIO
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union


class Element:
    """
    Representation of an XML element in an untangle object tree.

    Attributes:
        _name: The local tag name of the XML element.
        _attributes: Dictionary containing XML attributes key-value pairs.
        children: List of child Element instances.
        is_root: Boolean flag indicating if this is the root document element.
        cdata: Accumulated character data / text content within this element.
    """

    _name: Optional[str]
    _attributes: Dict[str, str]
    children: List['Element']
    is_root: bool
    cdata: str

    def __init__(self, name: Optional[str] = None, attributes: Optional[Dict[str, str]] = None) -> None:
        """
        Initialize an untangle XML Element.

        Args:
            name: Optional tag name of the element.
            attributes: Optional dictionary of element attributes.
        """
        ...

    def add_child(self, element: 'Element') -> None:
        """
        Append a child Element to this element's children list.

        Args:
            element: The child Element to add.
        """
        ...

    def add_cdata(self, cdata: str) -> None:
        """
        Append character data to this element's cdata buffer.

        Args:
            cdata: String text content to append.
        """
        ...

    def get_attribute(self, key: str) -> str:
        """
        Retrieve an XML attribute value by name.

        Args:
            key: The XML attribute name to look up.

        Returns:
            The string value of the attribute.
        """
        ...

    def get_elements(self, name: Optional[str] = None) -> Any:
        """
        Find child elements matching the given tag name, or all children if name is omitted.

        Args:
            name: Optional tag name to filter child elements by.

        Returns:
            A list of matching child Element objects.
        """
        ...

    def __getitem__(self, key: str) -> Any:
        """
        Retrieve an XML attribute value by key via dictionary indexing syntax: `element[key]`.

        Args:
            key: The XML attribute name to look up.

        Returns:
            The string value of the attribute.
        """
        ...

    def __getattr__(self, key: str) -> Any:
        """
        Retrieve child elements dynamically via dot notation: `element.ChildTag`.

        Args:
            key: The name of the child element to retrieve.

        Returns:
            The matching child Element or list of Elements.
        """
        ...

    def __hasattribute__(self, name: str) -> bool:
        """
        Check if an attribute or child element exists by name.

        Args:
            name: The attribute or child element name to check.

        Returns:
            True if present, False otherwise.
        """
        ...

    def __iter__(self) -> Iterator['Element']:
        """
        Yield this element for iteration.

        Returns:
            An iterator yielding this Element.
        """
        ...

    def __bool__(self) -> bool:
        """
        Boolean evaluation of element presence.

        Returns:
            True if element is root or has a valid name, False otherwise.
        """
        ...

    def __eq__(self, val: object) -> bool:
        """
        Equality comparison against element cdata content.

        Args:
            val: The value to compare against cdata.

        Returns:
            True if equal, False otherwise.
        """
        ...

    def __dir__(self) -> List[str]:
        """
        List child element names for introspection and autocomplete.

        Returns:
            List of child element tag names.
        """
        ...

    def __len__(self) -> int:
        """
        Return the number of child elements.

        Returns:
            Count of child elements.
        """
        ...

    def __contains__(self, key: str) -> bool:
        """
        Check if key exists in child element names.

        Args:
            key: The child element tag name to check.

        Returns:
            True if key is in dir(self), False otherwise.
        """
        ...


def parse(filename: Union[str, Path, StringIO], **parser_features: Any) -> Element:
    """
    Parse an XML document from a file path, URL, path-like object, or XML string.

    Args:
        filename: A filesystem path, URL, open file-like object, or raw XML string.
        **parser_features: Optional SAX parser feature flags.

    Returns:
        The root untangle Element representing the XML document structure.
    """
    ...
