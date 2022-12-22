from enum import Enum

from mappers.models import FieldTypeChoices


class JSONType(Enum):
    ARRAY = "array"
    OBJECT = "object"
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"


FIELD_TYPE_TO_JSON_TYPE = {
    FieldTypeChoices.LIST: JSONType.ARRAY,
    FieldTypeChoices.OBJECT: JSONType.OBJECT,
    FieldTypeChoices.STRING: JSONType.STRING,
    FieldTypeChoices.NUMBER: JSONType.NUMBER,
    FieldTypeChoices.BOOLEAN: JSONType.BOOLEAN,
}

JSON_TYPE_TO_FIELD_TYPE = {
    JSONType.ARRAY: FieldTypeChoices.LIST,
    JSONType.OBJECT: FieldTypeChoices.OBJECT,
    JSONType.STRING: FieldTypeChoices.STRING,
    JSONType.NUMBER: FieldTypeChoices.NUMBER,
    JSONType.BOOLEAN: FieldTypeChoices.BOOLEAN,
}
