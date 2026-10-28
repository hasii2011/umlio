
CUSTOMER_INSTANCE_ID:        str = 'customer.instance'
ORDER_SERVICE_INSTANCE_ID:   str = 'orderservice.instance'
MESSAGE_PLACE_ORDER_ID:      str = 'msg.placeorder'
EXECUTION_ORDER_SERVICE_ID:  str = 'exec.orderservice.1'
FRAGMENT_ALT_ID:             str = 'fragment.alt.1'

CUSTOMER_MODEL_ID:           str = 'inst-001'
ORDER_SERVICE_MODEL_ID:      str = 'inst-002'
MESSAGE_MODEL_ID:            str = 'sdmsg-001'
EXECUTION_MODEL_ID:          str = 'sdexec-001'

CUSTOMER_INSTANCE_NAME:      str = 'customer:Customer'
ORDER_SERVICE_INSTANCE_NAME: str = 'orderService:OrderService'
MESSAGE_TEXT:                str = 'placeOrder(orderId)'
EXECUTION_OPERATION_NAME:    str = 'placeOrder'

FRAGMENT_OPERATOR:           str = 'alt'
FRAGMENT_X:                  int = 80
FRAGMENT_Y:                  int = 160
FRAGMENT_WIDTH:              int = 380
FRAGMENT_HEIGHT:             int = 120

OPERAND_1_GUARD:             str = '[order != null]'
OPERAND_1_START_Y:           int = 160
OPERAND_1_END_Y:             int = 220

OPERAND_2_GUARD:             str = '[else]'
OPERAND_2_START_Y:           int = 220
OPERAND_2_END_Y:             int = 280

INSTANCE_Y:                  int = 60
CUSTOMER_INSTANCE_X:         int = 120
CUSTOMER_INSTANCE_WIDTH:     int = 100

ORDER_SERVICE_INSTANCE_X:     int = 340
ORDER_SERVICE_INSTANCE_WIDTH: int = 120

DEFAULT_LIFELINE_LENGTH:     int = 400

MESSAGE_TIME_STEP:           int = 120

EXECUTION_START_Y:           int = 120
EXECUTION_END_Y:             int = 260
EXECUTION_NESTING_LEVEL:     int = 0

EMPTY_SD_DIAGRAM_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Empty SD Diagram" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    '</UMLDiagram>'
)

EXPECTED_SD_INSTANCES_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDInstance id="{CUSTOMER_INSTANCE_ID}" width="{CUSTOMER_INSTANCE_WIDTH}" height="{DEFAULT_LIFELINE_LENGTH}" x="{CUSTOMER_INSTANCE_X}" y="{INSTANCE_Y}" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{CUSTOMER_MODEL_ID}" instanceName="{CUSTOMER_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDInstance id="{ORDER_SERVICE_INSTANCE_ID}" width="{ORDER_SERVICE_INSTANCE_WIDTH}" height="{DEFAULT_LIFELINE_LENGTH}" x="{ORDER_SERVICE_INSTANCE_X}" y="{INSTANCE_Y}" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{ORDER_SERVICE_MODEL_ID}" instanceName="{ORDER_SERVICE_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    '</UMLDiagram>'
)

EXPECTED_SD_MESSAGES_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDMessage id="{MESSAGE_PLACE_ORDER_ID}" messageType="Synchronous Message">\n'
    f'        <ModelSDMessage id="{MESSAGE_MODEL_ID}" message="{MESSAGE_TEXT}" sourceTime="{MESSAGE_TIME_STEP}" destinationTime="{MESSAGE_TIME_STEP}" sourceId="{CUSTOMER_MODEL_ID}" destinationId="{ORDER_SERVICE_MODEL_ID}" />\n'
    '    </UmlSDMessage>\n'
    '</UMLDiagram>'
)

EXPECTED_SD_EXECUTIONS_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDExecution id="{EXECUTION_ORDER_SERVICE_ID}">\n'
    f'        <ModelSDExecution id="{EXECUTION_MODEL_ID}" instanceId="{ORDER_SERVICE_MODEL_ID}" startTime="{EXECUTION_START_Y}" endTime="{EXECUTION_END_Y}" nestingLevel="{EXECUTION_NESTING_LEVEL}" operation="{EXECUTION_OPERATION_NAME}" />\n'
    '    </UmlSDExecution>\n'
    '</UMLDiagram>'
)

EXPECTED_SD_COMBINED_FRAGMENTS_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDCombinedFragment id="{FRAGMENT_ALT_ID}" width="{FRAGMENT_WIDTH}" height="{FRAGMENT_HEIGHT}" x="{FRAGMENT_X}" y="{FRAGMENT_Y}" operator="{FRAGMENT_OPERATOR}">\n'
    f'        <SDInteractionOperand guard="{OPERAND_1_GUARD}" startY="{OPERAND_1_START_Y}" endY="{OPERAND_1_END_Y}" />\n'
    f'        <SDInteractionOperand guard="{OPERAND_2_GUARD}" startY="{OPERAND_2_START_Y}" endY="{OPERAND_2_END_Y}" />\n'
    '    </UmlSDCombinedFragment>\n'
    '</UMLDiagram>'
)

EXPECTED_SEQUENCE_DIAGRAM_XML: str = (
    "<?xml version='1.0' encoding='iso-8859-1'?>\n"
    '<UMLDiagram documentType="Sequence Document" title="Order Processing" scrollPositionX="1" scrollPositionY="1" pixelsPerUnitX="1" pixelsPerUnitY="1">\n'
    f'    <UmlSDInstance id="{CUSTOMER_INSTANCE_ID}" width="{CUSTOMER_INSTANCE_WIDTH}" height="{DEFAULT_LIFELINE_LENGTH}" x="{CUSTOMER_INSTANCE_X}" y="{INSTANCE_Y}" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{CUSTOMER_MODEL_ID}" instanceName="{CUSTOMER_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDInstance id="{ORDER_SERVICE_INSTANCE_ID}" width="{ORDER_SERVICE_INSTANCE_WIDTH}" height="{DEFAULT_LIFELINE_LENGTH}" x="{ORDER_SERVICE_INSTANCE_X}" y="{INSTANCE_Y}" lifeLineLength="{DEFAULT_LIFELINE_LENGTH}">\n'
    f'        <ModelSDInstance id="{ORDER_SERVICE_MODEL_ID}" instanceName="{ORDER_SERVICE_INSTANCE_NAME}" />\n'
    '    </UmlSDInstance>\n'
    f'    <UmlSDMessage id="{MESSAGE_PLACE_ORDER_ID}" messageType="Synchronous Message">\n'
    f'        <ModelSDMessage id="{MESSAGE_MODEL_ID}" message="{MESSAGE_TEXT}" sourceTime="{MESSAGE_TIME_STEP}" destinationTime="{MESSAGE_TIME_STEP}" sourceId="{CUSTOMER_MODEL_ID}" destinationId="{ORDER_SERVICE_MODEL_ID}" />\n'
    '    </UmlSDMessage>\n'
    f'    <UmlSDExecution id="{EXECUTION_ORDER_SERVICE_ID}">\n'
    f'        <ModelSDExecution id="{EXECUTION_MODEL_ID}" instanceId="{ORDER_SERVICE_MODEL_ID}" startTime="{EXECUTION_START_Y}" endTime="{EXECUTION_END_Y}" nestingLevel="{EXECUTION_NESTING_LEVEL}" operation="{EXECUTION_OPERATION_NAME}" />\n'
    '    </UmlSDExecution>\n'
    f'    <UmlSDCombinedFragment id="{FRAGMENT_ALT_ID}" width="{FRAGMENT_WIDTH}" height="{FRAGMENT_HEIGHT}" x="{FRAGMENT_X}" y="{FRAGMENT_Y}" operator="{FRAGMENT_OPERATOR}">\n'
    f'        <SDInteractionOperand guard="{OPERAND_1_GUARD}" startY="{OPERAND_1_START_Y}" endY="{OPERAND_1_END_Y}" />\n'
    f'        <SDInteractionOperand guard="{OPERAND_2_GUARD}" startY="{OPERAND_2_START_Y}" endY="{OPERAND_2_END_Y}" />\n'
    '    </UmlSDCombinedFragment>\n'
    '</UMLDiagram>'
)
