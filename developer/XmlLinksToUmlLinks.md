# `XmlLinksToUmlLinks` Class

The `XmlLinksToUmlLinks` class is a deserializer responsible for converting `<UmlLink>` XML elements from a saved diagram file back into a list of graphical `UmlLink` objects. It reconstructs the links between shapes that have already been deserialized.

This class is the counterpart to `UmlLinksToXml` and is essential for loading saved diagrams by recreating the relationships and their visual paths between UML shapes.

## Key Responsibilities

*   Parsing `<UmlLink>` elements within a larger diagram XML structure.
*   Identifying the source and destination shapes for each link using a provided dictionary of existing shapes.
*   Re-creating the logical `Link` data model by collaborating with `XmlToUmlModel`.
*   Instantiating the correct graphical `UmlLink` subclass (e.g., `UmlAssociation`, `UmlInheritance`) based on the link's type.
*   Restoring the link's graphical properties, including its ID, spline status, and the control points that define its path.

## Deserialization Process & Dependencies

The deserialization process has a specific order. `XmlLinksToUmlLinks` must be called **after** all linkable shapes (like `UmlClass`, `UmlNote`, etc.) have already been deserialized.

*   **Dependency 1: `LinkableUmlShapes` Dictionary:** The `deserialize` method requires a dictionary mapping shape IDs to their corresponding `LinkableUmlShape` objects. This is used to look up and connect the source and destination ends of each link.
*   **Dependency 2: `XmlToUmlModel`:** It uses an instance of `XmlToUmlModel` to deserialize the underlying `<ModelLink>` element, which represents the logical data of the link, separate from its graphical representation.

## Usage Example

```python
from untangle import parse
from umlio.deserializer.XmlLinksToUmlLinks import XmlLinksToUmlLinks
from umlio.deserializer.XmlShapesToUmlShapes import XmlShapesToUmlShapes # Used to get shapes first

# Assume 'xml_file_path' is the path to a saved .xml diagram
xml_root = parse(xml_file_path)
diagram_element = xml_root.UmlProject.UMLDiagram

# 1. First, deserialize all the shapes
shape_deserializer = XmlShapesToUmlShapes()
linkable_shapes = shape_deserializer.getLinkableUmlShapes(diagram_element)

# 2. Now, deserialize the links using the created shapes
link_deserializer = XmlLinksToUmlLinks()
uml_links = link_deserializer.deserialize(
    umlDiagramElement=diagram_element,
    linkableUmlShapes=linkable_shapes
)

# The 'uml_links' variable now holds a list of reconstructed UmlLink objects
for link in uml_links:
    print(f"Recreated link: {link.id} from {link.sourceShape.id} to {link.destinationShape.id}")

```

## Public Methods

### `__init__(self)`

The constructor initializes the `XmlLinksToUmlLinks` deserializer. It also creates an instance of `XmlToUmlModel`, which it will use to handle the deserialization of the core `<ModelLink>` data.

### `deserialize(self, umlDiagramElement: Element, linkableUmlShapes: LinkableUmlShapes) -> UmlLinks`

This is the main public method that drives the deserialization of links. It finds all `<UmlLink>` elements within the provided `umlDiagramElement`, processes each one to reconstruct a `UmlLink` object, and returns them as a list.

*   **Parameters:**
    *   `umlDiagramElement` (`Element`): The parent XML element (`<UMLDiagram>`) containing the `<UmlLink>` elements to be processed.
    *   `linkableUmlShapes` (`LinkableUmlShapes`): A dictionary mapping the ID of every linkable shape in the diagram to its object instance.
*   **Returns:**
    *   `UmlLinks`: A list of the newly created `UmlLink` objects.

## Expected XML Input Structure

The class is designed to parse an XML structure like the following:

```xml
<UMLDiagram>
    <!-- ... UmlClass, UmlNote, and other shape elements ... -->
    
    <UmlLink id="link-123" fromX="100" fromY="150" toX="300" toY="150" spline="False">
        
        <!-- The underlying logical link -->
        <ModelLink 
            name="Has a" 
            type="ASSOCIATION" 
            sourceId="class-A" 
            destinationId="class-B" 
        />

        <!-- Optional control points that define the line's shape -->
        <ModelLineControlPoint x="200" y="120" />
    </UmlLink>

    <!-- ... more UmlLink elements ... -->
</UMLDiagram>
```