# Sequence Diagram Model Serialization: Transfer to `umlio`

## Architectural Decision

The responsibility for **Sequence Diagram Model Serialization (JSON / XML)**—including saving, loading, round-tripping diagram state, and persisting visual elements to file formats—is officially transferred out of `umlshapes` to the dedicated **`umlio`** repository (`/Users/humberto.a.sanchez.ii/PycharmProjects/umlio`).

---

## Separation of Responsibilities

### `umlshapes` (Rendering, Layout & User Interaction)
- **Visual Shapes:**
  - Participants: `UmlSDInstance`, `UmlSDLifeLine`, `UmlInstanceName`.
  - Messages: `UmlSDMessage` (Synchronous, Asynchronous, Return, Reflexive, Lost, Found).
  - Executions: `UmlSDExecution` (Activation Bars).
  - Combined Fragments: `UmlSDCombinedFragment` (`alt`, `opt`, `loop`, `par`, `break`).
- **Interactive Manipulation:**
  - Hit-testing, dragging, selection, and multi-handle control points.
  - Double-click dialogs (`DlgEditInstanceName`, message label editing).
- **Layout Calculations:**
  - `SDLayoutEngine`: Deterministic participant column placement, discrete time-step snapping, and fragment bounds.
- **Preferences:**
  - User preferences via `UmlPreferences` and `SDPreferencesPanel`.

### `umlio` (Persistence, I/O, & Data Interchange)
- **Serialization & Deserialization:**
  - Mapping sequence diagram models and layouts to/from JSON and XML file schemas.
- **Round-Trip State Persistence:**
  - Reading persisted files and instantiating diagram model elements.
  - Writing sequence diagram state, lifeline positions, message sequences, execution specifications, and fragment bounds to disk.
- **Interchange & Export:**
  - Format conversions, export utilities, and integrations with external tools.
