from abc import ABC, abstractmethod
from typing import Any

from mappers.exceptions import InvalidType
from mappers.models import FieldTypeChoices
from mappers.services.model_field_service import ModelFieldService


class AbstractFieldMapper(ABC):
    def __init__(self, service: ModelFieldService):
        self.remote_field_id = None
        self.remote_model_id = None
        self.service = service

    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def map_to_target(self, remote_value):
        pass

    @abstractmethod
    def map_to_json_type(self, dto):
        pass

    def set_remote_field_id(self, id):
        self.remote_field_id = id
        return self

    def set_remote_model_id(self, id):
        self.remote_model_id = id
        return self

    def get_json_type(self):
        return self.type.lower()


class JSONMapperFactory:
    def __init__(self, service: ModelFieldService = None):
        self.field_types = FieldTypeChoices
        self.service = service

    def add_service(self, service: ModelFieldService):
        self.service = service

    class ObjectFieldMapper(AbstractFieldMapper):
        type = FieldTypeChoices.OBJECT

        def map_to_target(self, remote_value: dict):
            result = {}

            remote_fields = self._get_fields_by_remote_model_id(self.remote_model_id)

            for remote_field in remote_fields:
                target_field = self.service.get_target_field_from_remote_id(
                    remote_field.id
                )
                target_field_key = target_field.name
                remote_field_key = remote_field.name
                field_mapper = JSONMapperFactory(self.service).get_mapper_by_type(
                    remote_field.get_type()
                )
                field_mapper.set_remote_field_id(remote_field.id).set_remote_model_id(
                    remote_field.object_model_id
                )
                result[target_field_key] = field_mapper.map_to_target(
                    remote_value[remote_field_key]
                )

            return result

        def _get_fields_by_remote_model_id(self, remote_model_id):
            remote_model = self.service.get_model_by_id(remote_model_id)
            return remote_model.fields.all() or []

        def map_to_json_type(self, dto):
            result = {"type": self.get_json_type(), "properties": {}}

            for k, v in dto.items():
                field_mapper = JSONMapperFactory(self.service).get_mapper_by_value(v)
                result["properties"][k] = field_mapper.map_to_json_type(v)

            return result

    class ListFieldMapper(AbstractFieldMapper):
        type = FieldTypeChoices.ARRAY

        def map_to_target(self, remote_value):
            result = []
            remote_field = self.service.get_field_by_id(self.remote_field_id)
            field_mapper = JSONMapperFactory(self.service).get_mapper_by_type(
                remote_field.get_list_item_type()
            )
            field_mapper.set_remote_model_id(remote_field.object_model_id)

            for value in remote_value:
                result.append(field_mapper.map_to_target(value))

            return result

        def map_to_json_type(self, dto):
            result = {
                "type": self.get_json_type(),
            }

            item = next(iter(dto), None)
            field_mapper = JSONMapperFactory(self.service).get_mapper_by_value(item)
            result["items"] = field_mapper.map_to_json_type(item)

            return result

    class PrimitiveFieldMapper(AbstractFieldMapper):
        def map_to_target(self, remote_value):
            return remote_value

        def map_to_json_type(self, dto):
            return {"type": self.get_json_type()}

    class NumberFieldMapper(PrimitiveFieldMapper):
        type = FieldTypeChoices.NUMBER

    class StringFieldMapper(PrimitiveFieldMapper):
        type = FieldTypeChoices.STRING

    def _get_type(self, value):
        if type(value) is str:
            return self.field_types.STRING
        elif type(value) in [int, float]:
            return self.field_types.NUMBER
        elif type(value) is list:
            return self.field_types.ARRAY
        elif type(value) is dict:
            return self.field_types.OBJECT
        else:
            return self.field_types.UNKNOWN

    def get_mapper_by_type(self, type: FieldTypeChoices):
        if type is self.field_types.OBJECT:
            return self.ObjectFieldMapper(self.service)
        elif type is self.field_types.ARRAY:
            return self.ListFieldMapper(self.service)
        elif type is self.field_types.NUMBER:
            return self.NumberFieldMapper(self.service)
        elif type is self.field_types.STRING:
            return self.StringFieldMapper(self.service)
        else:
            raise InvalidType(msg=f"Unprocessable field type: {type}")

    def get_mapper_by_value(self, value: Any):
        type = self._get_type(value)
        if type is self.field_types.OBJECT:
            return self.ObjectFieldMapper(self.service)
        elif type is self.field_types.ARRAY:
            return self.ListFieldMapper(self.service)
        elif type is self.field_types.NUMBER:
            return self.NumberFieldMapper(self.service)
        elif type is self.field_types.STRING:
            return self.StringFieldMapper(self.service)
        else:
            raise InvalidType(msg=f"Unprocessable value of type: {type}")
