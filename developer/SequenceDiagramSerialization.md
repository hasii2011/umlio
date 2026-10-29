# Sequence Diagram Serialization

## Overview

The `umlio` package is responsible for the persistence, I/O, and data interchange of UML diagrams. This document defines the architecture, XML schema, and component responsibilities for **Sequence Diagram Serialization** (converting in-memory sequence diagram shapes and models into XML format).

Serialization converts interactive visual shapes (`umlshapes.sd`) and their corresponding underlying data models (`umlmodel`) into structured XML using `xml.etree.ElementTree`.

---

## Foundation in `UmlModelToXml`

The logical data model serialization methods for Sequence Diagrams are implemented in `src/umlio/serializer/UmlModelToXml.py`:

- **`sdInstanceToXml(self, sdInstance: SDInstance, sdInstanceElement: Element) -> Element`**:
  Serializes `<ModelSDInstance>` with `id` and `instanceName`.
- **`sdMessageToXml(self, sdMessage: SDMessage, sdMessageElement: Element) -> Element`**:
  Serializes `<ModelSDMessage>` with `id`, `message`, `sourceTime`, `destinationTime`, `sourceId`, and `destinationId`.
- **`sdExecutionToXml(self, sdExecution: SDExecution, sdExecutionElement: Element) -> Element`**:
  Serializes `<ModelSDExecution>` with `id`, `instanceId`, `startTime`, `endTime`, `nestingLevel`, and `operation`.

---

## Target XML Output Schema

```xml
<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">

    <!-- SD Instance Shapes -->
    <UmlSDInstance id="customer.instance" x="120" y="60" width="100" height="50" lifeLineLength="400">
        <ModelSDInstance id="inst-001" instanceName="customer:Customer" />
    </UmlSDInstance>

    <UmlSDInstance id="orderservice.instance" x="340" y="60" width="120" height="50" lifeLineLength="400">
        <ModelSDInstance id="inst-002" instanceName="orderService:OrderService" />
    </UmlSDInstance>

    <!-- Sequence Messages -->
    <UmlSDMessage id="msg.placeorder" messageType="Synchronous Message">
        <ModelSDMessage id="sdmsg-001" message="placeOrder(orderId)" sourceId="customer.instance" destinationId="orderservice.instance" sourceTime="120" destinationTime="120" />
    </UmlSDMessage>

    <UmlSDMessage id="msg.orderack" messageType="Return Message">
        <ModelSDMessage id="sdmsg-002" message="orderConfirmation" sourceId="orderservice.instance" destinationId="customer.instance" sourceTime="260" destinationTime="260" />
    </UmlSDMessage>

    <!-- Execution Specifications (Activation Bars) -->
    <UmlSDExecution id="exec.orderservice.1">
        <ModelSDExecution id="sdexec-001" instanceId="orderservice.instance" startTime="120" endTime="260" nestingLevel="0" operation="placeOrder" />
    </UmlSDExecution>

    <!-- Combined Fragments -->
    <UmlSDCombinedFragment id="fragment.alt.1" operator="alt" x="80" y="160" width="380" height="120">
        <SDInteractionOperand guard="[order != null]" startY="160" endY="220" />
        <SDInteractionOperand guard="[else]" startY="220" endY="280" />
    </UmlSDCombinedFragment>

    <!-- Standard Text and Note annotations -->
    <UmlText id="sd.annotation" x="50" y="20" width="200" height="30">
        <ModelText id="text-001" content="Main checkout scenario" />
    </UmlText>

</UMLDiagram>
```

---

## Serialization Pipeline & Component Breakdown

All visual shape serializers inherit from `BaseUmlToXml` and utilize `SubElement` to append elements to `documentTop`.

```
UmlShapesToXml.serialize(umlDiagram)
  ├── UmlSDInstancesToXml.serialize(documentTop, umlDiagram.umlSDInstances)
  │     └── UmlModelToXml.sdInstanceToXml()
  ├── UmlSDMessagesToXml.serialize(documentTop, umlDiagram.umlSDMessages)
  │     └── UmlModelToXml.sdMessageToXml()
  ├── UmlSDExecutionsToXml.serialize(documentTop, umlDiagram.umlSDExecutions)
  │     └── UmlModelToXml.sdExecutionToXml()
  ├── UmlSDCombinedFragmentsToXml.serialize(documentTop, umlDiagram.umlSDCombinedFragments)
  ├── UmlTextsToXml.serialize(documentTop, umlDiagram.umlTexts)
  └── UmlNotesToXml.serialize(documentTop, umlDiagram.umlNotes)
```

### 1. `UmlSDInstancesToXml` (`BaseUmlToXml`)
* **Input**: `documentTop` (`Element`), `umlSDInstances` (`UmlSDInstances`).
* **Responsibilities**:
  * Iterate over each `UmlSDInstance`.
  * Extract base shape attributes (`id`, `x`, `y`, `width`, `height`) via `_umlBaseAttributes()`.
  * Add visual `lifeLineLength` attribute from `umlSDInstance.getLifeLineLength()`.
  * Create `<UmlSDInstance>` `SubElement`.
  * Delegate underlying model persistence to `UmlModelToXml.sdInstanceToXml()`.

### 2. `UmlSDMessagesToXml` (`BaseUmlToXml`)
* **Input**: `documentTop` (`Element`), `umlSDMessages` (`UmlSDMessages`).
* **Responsibilities**:
  * Iterate over each `UmlSDMessage`.
  * Create `<UmlSDMessage>` `SubElement` with attributes `id` and `messageType`.
  * Ensure `sdMessage.source` and `sdMessage.destination` link IDs reference the enclosing `UmlSDInstance` monikers.
  * Delegate underlying model persistence to `UmlModelToXml.sdMessageToXml()`.

### 3. `UmlSDExecutionsToXml` (`BaseUmlToXml`)
* **Input**: `documentTop` (`Element`), `umlSDExecutions` (`UmlSDExecutions`).
* **Responsibilities**:
  * Iterate over each `UmlSDExecution`.
  * Create `<UmlSDExecution>` `SubElement` with attribute `id`.
  * Delegate underlying model persistence to `UmlModelToXml.sdExecutionToXml()`.

### 4. `UmlSDCombinedFragmentsToXml` (`BaseUmlToXml`)
* **Input**: `documentTop` (`Element`), `umlSDCombinedFragments` (`UmlSDCombinedFragments`).
* **Responsibilities**:
  * Iterate over each `UmlSDCombinedFragment`.
  * Extract bounding coordinates via `_umlBaseAttributes()`.
  * Create `<UmlSDCombinedFragment>` `SubElement` with attributes: `id`, `operator`, `x`, `y`, `width`, `height`.
  * Iterate over `fragment.operands` and serialize each `<SDInteractionOperand>` with `guard`, `startY`, and `endY`.

---

## Integration into `UmlShapesToXml`

In `src/umlio/serializer/UmlShapesToXml.py`:
- Add instances of `UmlSDInstancesToXml`, `UmlSDMessagesToXml`, `UmlSDExecutionsToXml`, and `UmlSDCombinedFragmentsToXml`.
- Invoke them within `serialize(umlDiagram)` using `umlDiagram.umlSDInstances`, `umlDiagram.umlSDMessages`, `umlDiagram.umlSDExecutions`, and `umlDiagram.umlSDCombinedFragments`.

---

## Phased Implementation Roadmap

1. **Phase 1: `UmlSDInstancesToXml`**
   - Create `src/umlio/serializer/UmlSDInstancesToXml.py`.
2. **Phase 2: `UmlSDMessagesToXml`**
   - Create `src/umlio/serializer/UmlSDMessagesToXml.py`.
3. **Phase 3: `UmlSDExecutionsToXml`**
   - Create `src/umlio/serializer/UmlSDExecutionsToXml.py`.
4. **Phase 4: `UmlSDCombinedFragmentsToXml`**
   - Create `src/umlio/serializer/UmlSDCombinedFragmentsToXml.py`.
5. **Phase 5: Integration & Verification**
   - Update `UmlShapesToXml.py` to invoke all sequence diagram serializers.
   - Add sequence diagram serialization unit tests in `tests/umlio/TestWriter.py`.
