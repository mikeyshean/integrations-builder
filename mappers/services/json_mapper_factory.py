from abc import ABC, abstractmethod
from typing import Any, TypeVar

from mappers.constants import FIELD_TYPE_TO_JSON_TYPE
from mappers.exceptions import InvalidType
from mappers.models import Field, FieldTypeChoices
from mappers.services.map_service import MapService
from mappers.services.model_field_service import ModelFieldService

T = TypeVar("T", bound="JSONMapper")


class JSONMapper(ABC):
    def __init__(self, model_field_service: ModelFieldService, map_service: MapService):
        self.model_field_service = model_field_service
        self.map_service = map_service
        self._source_field_id = None
        self._source_model_id = None
        self._source_field = None
        self._map_id = None

    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def map_to_target(self, source_value):
        pass

    @abstractmethod
    def map_to_json_type_definition(self, dto):
        pass

    @property
    def source_field_id(self) -> int:
        return self._source_field_id

    @property
    def source_model_id(self) -> int:
        return self._source_model_id

    @property
    def source_field(self) -> Field:
        result = self._source_field
        if not result:
            result = self.model_field_service.get_field_by_id(self.source_field_id)
        return result

    @property
    def map_id(self) -> int:
        return self._map_id

    def set_source_model_id(self: T, id: int) -> T:
        self._source_model_id = id
        return self

    def set_source_field_id(self: T, id: int) -> T:
        self._source_field_id = id
        return self

    def set_map_id(self: T, id: int) -> T:
        self._map_id = id
        return self

    def get_json_type(self: T) -> str:
        return FIELD_TYPE_TO_JSON_TYPE[self.type].value


class ObjectMapper(JSONMapper):
    type = FieldTypeChoices.OBJECT

    def map_to_target(self, source_value: dict) -> dict:
        """Maps a source data dict into the target model dict \
            This will be the usual entry point to recursively build \
            a complete target dto as we get a new mapper and call \
            `map_to_target` on each property of `source_value`

        Args:
            source_value (dict): Source dict to be mapped into target dto

        Returns:
            dict: target model dto
        """

        result = {}
        source_fields = self.model_field_service.get_fields_by_model_id(
            self.source_model_id
        )

        for source_field in source_fields:
            field_mapper = JSONMapperFactory(
                model_field_service=self.model_field_service,
                map_service=self.map_service,
            ).get_mapper_by_type(source_field.get_type())

            field_mapper.set_source_field_id(source_field.id).set_source_model_id(
                source_field.object_model_id
            ).set_map_id(self.map_id)

            target_field = self.map_service.get_target_field(
                source_field=source_field, map_id=self.map_id
            )
            result[target_field.name] = field_mapper.map_to_target(
                source_value[source_field.name]
            )

        return result

    def map_to_json_type_definition(self, dto):
        result = {"type": self.get_json_type(), "properties": {}}

        for k, v in dto.items():
            field_mapper = JSONMapperFactory(
                model_field_service=self.model_field_service,
                map_service=self.map_service,
            ).get_mapper_by_value(v)
            result["properties"][k] = field_mapper.map_to_json_type_definition(v)

        return result


class ListMapper(JSONMapper):
    type = FieldTypeChoices.LIST

    def map_to_target(self, source_value):
        result = []
        source_field = self.model_field_service.get_field_by_id(self.source_field_id)
        field_mapper = JSONMapperFactory(
            model_field_service=self.model_field_service, map_service=self.map_service
        ).get_mapper_by_type(source_field.get_list_item_type())
        field_mapper.set_source_model_id(
            source_field.object_model_id
        ).set_source_field_id(source_field.id).set_map_id(self.map_id)

        for value in source_value:
            result.append(field_mapper.map_to_target(value))

        return result

    def map_to_json_type_definition(self, dto):
        result = {
            "type": self.get_json_type(),
        }

        item = next(iter(dto), None)
        field_mapper = JSONMapperFactory(
            model_field_service=self.model_field_service, map_service=self.map_service
        ).get_mapper_by_value(item)
        result["items"] = field_mapper.map_to_json_type_definition(item)

        return result


class PrimitiveMapper(JSONMapper):
    def map_to_target(self, source_value):
        return self.map_service.transform(
            source_field=self.source_field,
            map_id=self.map_id,
            source_value=source_value,
        )

    def map_to_json_type_definition(self, dto):
        return {"type": self.get_json_type()}


class NumberMapper(PrimitiveMapper):
    type = FieldTypeChoices.NUMBER


class StringMapper(PrimitiveMapper):
    type = FieldTypeChoices.STRING


class JSONMapperFactory:
    def __init__(
        self,
        map_service: MapService,
        model_field_service: ModelFieldService = None,
    ):
        self.field_types = FieldTypeChoices
        self._model_field_service = model_field_service
        self.map_service = map_service

    @property
    def model_field_service(self):
        return self._model_field_service

    def set_model_field_service(self, model_field_service: ModelFieldService):
        self._model_field_service = model_field_service

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
            return ObjectMapper(self.model_field_service, self.map_service)
        elif type is self.field_types.LIST:
            return ListMapper(self.model_field_service, self.map_service)
        elif type is self.field_types.NUMBER:
            return NumberMapper(self.model_field_service, self.map_service)
        elif type is self.field_types.STRING:
            return StringMapper(self.model_field_service, self.map_service)
        else:
            raise InvalidType(msg=f"Unprocessable field type: {type}")

    def get_mapper_by_value(self, value: Any):
        type = self._get_type(value)
        if type is self.field_types.OBJECT:
            return ObjectMapper(self.model_field_service, self.map_service)
        elif type is self.field_types.LIST:
            return ListMapper(self.model_field_service, self.map_service)
        elif type is self.field_types.NUMBER:
            return NumberMapper(self.model_field_service, self.map_service)
        elif type is self.field_types.STRING:
            return StringMapper(self.model_field_service, self.map_service)
        else:
            raise InvalidType(msg=f"Unprocessable value of type: {type}")
