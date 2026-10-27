# Sequence Diagram Deserialization

## Overview

The `umlio` package is responsible for the persistence, I/O, and data interchange of UML diagrams. This document defines the architecture, XML schema, and component responsibilities for **Sequence Diagram Deserialization** (loading and reconstructing sequence diagrams from XML).

Sequence diagram deserialization reconstructs interactive visual shapes (`umlshapes.sd`) and their corresponding underlying data models (`umlmodel`) from serialized XML.

---

## Separation of Responsibilities

- **`umlmodel`**: Stores core domain data:
  - `SDInstance`: Instance moniker, name, lifeline length, and instance graphical type (Class or Actor).
  - `SDMessage`: Message text, source and destination endpoints, and time/vertical offsets.
- **`umlshapes.sd`**: Provides interactive visual canvas representations:
  - SD Instances: `UmlSDInstance`, `UmlSDLifeLine`, `UmlInstanceName`.
  - Messages: `UmlSDMessage` (Synchronous, Asynchronous, Return, Reflexive, Lost, Found).
  - Executions: `UmlSDExecution` (Activation Bars).
  - Combined Fragments: `UmlSDCombinedFragment` (`alt`, `opt`, `loop`, `par`, `break`).
- **`umlio.deserializer`**: Parses diagram XML and instantiates visual shapes and underlying models.

---

## Target XML Schema

```xml
<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">

    <!-- SD Instance Shapes -->
    <UmlSDInstance id="customer.instance" x="120" y="60" width="100" height="50">
        <ModelSDInstance id="inst-001" instanceName="customer:Customer" lifeLineLength="400" />
    </UmlSDInstance>

    <UmlSDInstance id="orderservice.instance" x="340" y="60" width="120" height="50">
        <ModelSDInstance id="inst-002" instanceName="orderService:OrderService" lifeLineLength="400" />
    </UmlSDInstance>

    <!-- Sequence Messages -->
    <UmlSDMessage id="msg.placeorder" messageType="Synchronous Message" fromX="120" fromY="120" toX="340" toY="120">
        <ModelSDMessage id="sdmsg-001" message="placeOrder(orderId)" sourceId="customer.instance" destinationId="orderservice.instance" sourceTime="120" destinationTime="120" />
    </UmlSDMessage>

    <UmlSDMessage id="msg.orderack" messageType="Return Message" fromX="340" fromY="260" toX="120" toY="260">
        <ModelSDMessage id="sdmsg-002" message="orderConfirmation" sourceId="orderservice.instance" destinationId="customer.instance" sourceTime="260" destinationTime="260" />
    </UmlSDMessage>

    <!-- Execution Specifications (Activation Bars) -->
    <UmlSDExecution id="exec.orderservice.1" attachedToId="orderservice.instance" startY="120" endY="260" nestingLevel="0" />

    <!-- Combined Fragments -->
    <UmlSDCombinedFragment id="fragment.alt.1" operator="alt" x="80" y="160" width="380" height="120">
        <SDInteractionOperand id="operand.1" guard="[order != null]" startY="160" endY="220" />
        <SDInteractionOperand id="operand.2" guard="[else]" startY="220" endY="280" />
    </UmlSDCombinedFragment>

    <!-- Standard Text and Note annotations -->
    <UmlText id="sd.annotation" x="50" y="20" width="200" height="30">
        <ModelText id="text-001" content="Main checkout scenario" />
    </UmlText>

</UMLDiagram>
```

---

## Deserialization Pipeline & Component Breakdown

Sequence diagram deserialization follows a strict dependency order:
1. **Instances First**: Deserialized first so their lifelines and coordinate anchors exist.
2. **Messages Second**: Connected between lifelines of existing instances.
3. **Executions Third**: Anchored to specific lifelines across given vertical ranges (`startY` to `endY`).
4. **Fragments Fourth**: Placed over lifelines and message regions with operands and guards.

```
XmlToUmlShapes.deserializeXml()
  └── [documentType == 'Sequence Document']
        ├── XmlSDInstancesToUmlSDInstances.deserialize()
        │     └── XmlToUmlModel.sdInstanceToModelSDInstance()
        ├── XmlSDMessagesToUmlSDMessages.deserialize(instances)
        │     └── XmlToUmlModel.sdMessageToModelSDMessage()
        ├── XmlSDExecutionsToUmlSDExecutions.deserialize(instances)
        ├── XmlSDFragmentsToUmlSDCombinedFragments.deserialize()
        ├── XmlTextsToUmlTexts.deserialize()
        └── XmlNotesToUmlNotes.deserialize()
```

### 1. `XmlSDInstancesToUmlSDInstances`
* **Input**: `<UMLDiagram>` untangle `Element`.
* **Output**: `UmlSDInstances` (`List[UmlSDInstance]`).
* **Responsibilities**:
  * Extract `<UmlSDInstance>` attributes: `id`, `x`, `y`, `width`, `height`.
  * Parse `<ModelSDInstance>` attributes: `instanceName`, `lifeLineLength`.
  * Construct `SDInstance` data model.
  * Instantiate `UmlSDInstance` with appropriate canvas/frame reference and lifeline length.

### 2. `XmlSDMessagesToUmlSDMessages`
* **Input**: `<UMLDiagram>` untangle `Element`, mapping of instance IDs to `UmlSDInstance`.
* **Output**: `UmlSDMessages` (`List[UmlSDMessage]`).
* **Responsibilities**:
  * Extract `<UmlSDMessage>` attributes: `id`, `messageType`, endpoint coordinates (`fromX`, `fromY`, `toX`, `toY`).
  * Parse `<ModelSDMessage>` attributes: `id`, `message`, `sourceId`, `destinationId`, `sourceTime`, `destinationTime`.
  * Resolve source and destination instances / lifelines.
  * Map `messageType` to `SDMessageType` enum (`SYNCHRONOUS`, `ASYNCHRONOUS`, `RETURN`, `REFLEXIVE`, `LOST`, `FOUND`).
  * Construct `SDMessage` model and instantiate `UmlSDMessage`.

### 3. `XmlSDExecutionsToUmlSDExecutions`
* **Input**: `<UMLDiagram>` untangle `Element`, mapping of instance IDs to `UmlSDInstance`.
* **Output**: `UmlSDExecutions` (`List[UmlSDExecution]`).
* **Responsibilities**:
  * Extract `<UmlSDExecution>` attributes: `id`, `attachedToId`, `startY`, `endY`, `nestingLevel`.
  * Locate target `UmlSDLifeLine` on the referenced `UmlSDInstance`.
  * Instantiate `UmlSDExecution(lifeLine=..., startY=..., endY=..., nestingLevel=...)`.

### 4. `XmlSDFragmentsToUmlSDCombinedFragments`
* **Input**: `<UMLDiagram>` untangle `Element`.
* **Output**: `UmlSDCombinedFragments` (`List[UmlSDCombinedFragment]`).
* **Responsibilities**:
  * Extract `<UmlSDCombinedFragment>` attributes: `id`, `operator`, `x`, `y`, `width`, `height`.
  * Map `operator` string to `SDFragmentOperator` (`ALT`, `OPT`, `LOOP`, `PAR`, `BREAK`).
  * Parse child `<SDInteractionOperand>` elements with guards and vertical bounds.
  * Instantiate `UmlSDCombinedFragment` and configure its operands.

---

## Data Structures in `umlio.IOTypes`

Additions to `src/umlio/IOTypes.py`:

```python
UmlSDInstances         = NewType('UmlSDInstances', List[UmlSDInstance])
UmlSDMessages          = NewType('UmlSDMessages', List[UmlSDMessage])
UmlSDExecutions        = NewType('UmlSDExecutions', List[UmlSDExecution])
UmlSDCombinedFragments = NewType('UmlSDCombinedFragments', List[UmlSDCombinedFragment])
```

Fields added to `UmlDocument`:

```python
umlSDInstances:         UmlSDInstances         = field(default_factory=umlSDInstancesFactory)
umlSDMessages:          UmlSDMessages          = field(default_factory=umlSDMessagesFactory)
umlSDExecutions:        UmlSDExecutions        = field(default_factory=umlSDExecutionsFactory)
umlSDCombinedFragments: UmlSDCombinedFragments = field(default_factory=umlSDCombinedFragmentsFactory)
```

---

## Phased Implementation Roadmap

1. **Phase 1A: Types & Constants Foundation**
   - Update `XMLConstants.py` with SD element and attribute strings.
   - Update `IOTypes.py` with SD NewTypes, factories, and `UmlDocument` fields.
   - Extend `XmlToUmlModel.py` for complete SD model deserialization.
2. **Phase 1B: Instance & Message Deserializers**
   - Create `XmlSDInstancesToUmlSDInstances.py`.
   - Create `XmlSDMessagesToUmlSDMessages.py`.
3. **Phase 1C: Executions & Combined Fragments Deserializers**
   - Create `XmlSDExecutionsToUmlSDExecutions.py`.
   - Create `XmlSDFragmentsToUmlSDCombinedFragments.py`.
4. **Phase 1D: Integration & Verification**
   - Integrate SD deserializers into `XmlToUmlShapes.py`.
   - Provide golden test XML files in `tests/resources/goldenfiles/`.
   - Add comprehensive unit tests in `tests/umlio/deserializer/TestSequenceDiagramDeserialization.py`.
