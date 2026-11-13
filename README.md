[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/hasii2011/umlio/graphs/commit-activity)
[![CI](https://github.com/hasii2011/umlio/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/hasii2011/umlio/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/umlio.svg)](https://badge.fury.io/py/umlio)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Copilot: No](https://img.shields.io/badge/GitHub_Copilot-No-red?logo=github&style=flat-square)](https://github.com/hasii2011/code-ally-basic/wiki/GitHub-Copilot)

# Introduction

`umlio` provides a Python serialization and deserialization layer for [UML Diagrammer](https://github.com/hasii2011/umldiagrammer) `.udt` (compressed project) and `.xml` files (currently XML format `14.0`). It is the updated successor to [oglio](https://github.com/hasii2011/oglio) and bridges [umlmodel](https://github.com/hasii2011/umlmodel) and [umlshapes](https://github.com/hasii2011/umlshapes).

## Supported Diagrams

- **Class Diagrams** (`UmlDocumentType.CLASS_DOCUMENT`): classes, notes, text labels, lollipop interfaces, and links (associations, aggregations, compositions, inheritance, interface realization, and note links).
- **Use Case Diagrams** (`UmlDocumentType.USE_CASE_DOCUMENT`): actors, use cases, notes, text labels, and links.
- **Sequence Diagrams** (`UmlDocumentType.SEQUENCE_DOCUMENT`): instances/lifelines, messages, executions, combined fragments, notes, and text labels.

# Installation

Requires Python 3.13 and `wxPython>=4.3.2`:

```bash
pip install umlio
```

For local development with test and packaging dependencies:

```bash
pip install -e '.[test,deploy]'
```

# Usage

Use `Reader` to load `.udt` or `.xml` files into an `UmlProject`, and `Writer` to serialize an `UmlProject` back to disk:

```python
from pathlib import Path

from umlio.IOTypes import UmlProject
from umlio.Reader import Reader
from umlio.Writer import Writer

reader: Reader = Reader()
umlProject: UmlProject = reader.readProjectFile(fileName=Path('MyProject.udt'))

writer: Writer = Writer()
writer.writeFile(umlProject=umlProject, fileName=Path('MyProjectCopy.udt'))
writer.writeXmlFile(umlProject=umlProject, fileName=Path('MyProjectCopy.xml'))
```

# Development & Verification

Run type checks and the unit test suite from the project root:

```bash
mypy --config-file .mypi.ini --check-untyped-defs src/umlio tests
PYTHONPATH=src:. python -m unittest discover -s tests -t . -p 'Test*.py' -v
```

*(On headless Linux, prefix the test command with `xvfb-run -a` for wxPython.)*

___

Written by <a href="mailto:humberto.a.sanchez.ii@gmail.com?subject=Hello Humberto">Humberto A. Sanchez II</a> (C) 2026
___

## Note
For all kinds of problems, requests, enhancements, bug reports, etc., please drop me an e-mail.


> [!NOTE]
> **I do not consent to GitHub's use of this project's code in Copilot.** See our [GitHub Copilot Statement](https://github.com/hasii2011/code-ally-basic/wiki/GitHub-Copilot) for details.
