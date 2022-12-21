from abc import ABC, abstractmethod
from typing import Any, TypeVar

from mappers.constants import FIELD_TYPE_TO_JSON_TYPE
from mappers.exceptions import InvalidType
from mappers.models import Field, FieldTypeChoices
from mappers.services.model_field_service import ModelFieldService
from mappers.services.transformer_service import TransformerService

T = TypeVar("T", bound="JSONMapper")


class JSONMapper(ABC):
    def __init__(
        self,
        transformer_service: TransformerService,
        model_field_service: ModelFieldService,
    ):
        self._transformer_service = transformer_service
        self._model_field_service = model_field_service
        self._remote_field_id = None
        self._remote_model_id = None
        self._remote_field = None

    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def map_to_target(self, remote_value):
        pass

    @abstractmethod
    def map_to_json_type_definition(self, dto):
        pass

    @property
    def remote_field_id(self) -> int:
        return self._remote_field_id

    @property
    def remote_model_id(self) -> int:
        return self._remote_model_id

    @property
    def remote_field(self) -> Field:
        result = self._remote_field
        if not result:
            result = self._model_field_service.get_field_by_id(self.remote_field_id)
        return result

    def set_remote_model_id(self: T, id: int) -> T:
        self._remote_model_id = id
        return self

    def set_remote_field_id(self: T, id) -> T:
        self._remote_field_id = id
        return self

    def get_json_type(self: T) -> str:
        return FIELD_TYPE_TO_JSON_TYPE[self.type].value


class ObjectMapper(JSONMapper):
    type = FieldTypeChoices.OBJECT

    def map_to_target(self, remote_value: dict):
        result = {}

        remote_fields = self._get_fields_by_remote_model_id(self.remote_model_id)

        for remote_field in remote_fields:
            target_field = self._model_field_service.get_target_field_from_remote_id(
                remote_field.id
            )
            target_field_key = target_field.name
            remote_field_key = remote_field.name
            field_mapper = JSONMapperFactory(
                self._transformer_service, self._model_field_service
            ).get_mapper_by_type(remote_field.get_type())
            field_mapper.set_remote_field_id(remote_field.id).set_remote_model_id(
                remote_field.object_model_id
            )
            result[target_field_key] = field_mapper.map_to_target(
                remote_value[remote_field_key]
            )

        return result

    def _get_fields_by_remote_model_id(self, remote_model_id):
        remote_model = self._model_field_service.get_model_by_id(remote_model_id)
        return remote_model.fields.all() or []

    def map_to_json_type_definition(self, dto):
        result = {"type": self.get_json_type(), "properties": {}}

        for k, v in dto.items():
            field_mapper = JSONMapperFactory(
                self._transformer_service, self._model_field_service
            ).get_mapper_by_value(v)
            result["properties"][k] = field_mapper.map_to_json_type_definition(v)

        return result


class ListMapper(JSONMapper):
    type = FieldTypeChoices.LIST

    def map_to_target(self, remote_value):
        result = []
        remote_field = self._model_field_service.get_field_by_id(self.remote_field_id)
        field_mapper = JSONMapperFactory(
            self._transformer_service, self._model_field_service
        ).get_mapper_by_type(remote_field.get_list_item_type())
        field_mapper.set_remote_model_id(
            remote_field.object_model_id
        ).set_remote_field_id(remote_field.id)

        for value in remote_value:
            result.append(field_mapper.map_to_target(value))

        return result

    def map_to_json_type_definition(self, dto):
        result = {
            "type": self.get_json_type(),
        }

        item = next(iter(dto), None)
        field_mapper = JSONMapperFactory(
            self._transformer_service, self._model_field_service
        ).get_mapper_by_value(item)
        result["items"] = field_mapper.map_to_json_type_definition(item)

        return result


class PrimitiveMapper(JSONMapper):
    def map_to_target(self, remote_value):
        return self._transform(remote_value)

    def _transform(self, remote_value):
        result = remote_value
        if self.remote_field.is_transformable():
            result = self._transformer_service.transform(
                id=self.remote_field.transformer_id, value=remote_value
            )
        return result

    def map_to_json_type_definition(self, dto):
        return {"type": self.get_json_type()}


class NumberMapper(PrimitiveMapper):
    type = FieldTypeChoices.NUMBER


class StringMapper(PrimitiveMapper):
    type = FieldTypeChoices.STRING


class JSONMapperFactory:
    def __init__(
        self,
        transformer_service: TransformerService,
        model_field_service: ModelFieldService = None,
    ):
        self.field_types = FieldTypeChoices
        self._model_field_service = model_field_service
        self._transformer_service = transformer_service

    def add_service(self, service: ModelFieldService):
        self._model_field_service = service

    def _get_type(self, value):
        if type(value) is str:
            return self.field_types.STRING
        elif type(value) in [int, float]:
            return self.field_types.NUMBER
        elif type(value) is list:
            return self.field_types.LIST
        elif type(value) is dict:
            return self.field_types.OBJECT
        else:
            return self.field_types.UNKNOWN

    def get_mapper_by_type(self, type: FieldTypeChoices):
        if type is self.field_types.OBJECT:
            return ObjectMapper(self._transformer_service, self._model_field_service)
        elif type is self.field_types.LIST:
            return ListMapper(self._transformer_service, self._model_field_service)
        elif type is self.field_types.NUMBER:
            return NumberMapper(self._transformer_service, self._model_field_service)
        elif type is self.field_types.STRING:
            return StringMapper(self._transformer_service, self._model_field_service)
        else:
            raise InvalidType(msg=f"Unprocessable field type: {type}")

    def get_mapper_by_value(self, value: Any):
        type = self._get_type(value)
        if type is self.field_types.OBJECT:
            return ObjectMapper(self._transformer_service, self._model_field_service)
        elif type is self.field_types.LIST:
            return ListMapper(self._transformer_service, self._model_field_service)
        elif type is self.field_types.NUMBER:
            return NumberMapper(self._transformer_service, self._model_field_service)
        elif type is self.field_types.STRING:
            return StringMapper(self._transformer_service, self._model_field_service)
        else:
            raise InvalidType(msg=f"Unprocessable value of type: {type}")
