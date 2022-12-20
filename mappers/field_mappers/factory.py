from abc import ABC, abstractmethod
from typing import Any

from mappers.models import FieldTypeChoices
from mappers.repository import MappingRepository


class AbstractFieldMapper(ABC):
    def __init__(self, mapping_repository: MappingRepository):
        self.mapping_repository = mapping_repository
        self.remote_field_id = None
        self.remote_model_id = None

    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def map_to_target(self, source_value):
        pass

    @abstractmethod
    def map_to_type(self, source_value):
        pass

    def set_remote_field_id(self, id):
        self.remote_field_id = id
        return self

    def set_remote_model_id(self, id):
        self.remote_model_id = id
        return self


class ObjectFieldMapper(AbstractFieldMapper):
    type = FieldTypeChoices.OBJECT

    def map_to_target(self, source_value: dict):
        result = {}

        remote_fields = self._get_fields_by_remote_model_id(self.remote_model_id)

        for remote_field in remote_fields:
            target_field = self.mapping_repository.get_target_field_by_id(
                remote_field["target_field_id"]
            )
            target_field_key = target_field["name"]
            remote_field_key = remote_field["name"]

            field_mapper = FieldMapperFactory(
                self.mapping_repository
            ).get_mapper_by_type(remote_field["type"])
            field_mapper.set_remote_field_id(remote_field["id"]).set_remote_model_id(
                remote_field["object_model_id"]
            )
            result[target_field_key] = field_mapper.map_to_target(
                source_value[remote_field_key]
            )

        return result

    def _get_fields_by_remote_model_id(self, remote_model_id):
        remote_model = self.mapping_repository.get_remote_model_by_id(remote_model_id)
        return remote_model["fields"] or []

    def map_to_type(self, source_value):
        result = {"type": self.type, "properties": {}}

        for k, v in source_value.items():
            field_mapper = FieldMapperFactory(
                self.mapping_repository
            ).get_mapper_by_value(v)
            result["properties"][k] = field_mapper.map_to_type(v)

        return result


class ListFieldMapper(AbstractFieldMapper):
    type = FieldTypeChoices.ARRAY

    def map_to_target(self, source_value):
        result = []
        remote_field = self.mapping_repository.get_remote_field_by_id(
            self.remote_field_id
        )
        list_item_type = remote_field["list_item_type"]
        field_mapper = FieldMapperFactory(self.mapping_repository).get_mapper_by_type(
            list_item_type
        )
        field_mapper.set_remote_model_id(remote_field["object_model_id"])

        for value in source_value:
            result.append(field_mapper.map_to_target(value))

        return result

    def map_to_type(self, source_value):
        result = {
            "type": self.type,
        }

        item = next(iter(source_value), None)
        field_mapper = FieldMapperFactory(self.mapping_repository).get_mapper_by_value(
            item
        )
        result["items"] = field_mapper.map_to_type(item)

        return result


class PrimitiveFieldMapper(AbstractFieldMapper):
    def map_to_target(self, source_value):
        return source_value

    def map_to_type(self, source_value):
        return {"type": self.type}


class NumberFieldMapper(PrimitiveFieldMapper):
    type = FieldTypeChoices.NUMBER


class StringFieldMapper(PrimitiveFieldMapper):
    type = FieldTypeChoices.STRING


class FieldMapperFactory:
    def __init__(self, repository: MappingRepository):
        self.field_types = FieldTypeChoices
        self.repository = repository

    def _get_type(self, value):
        if type(value) is str:
            return self.field_types.STRING
        elif type(value) in [int, float]:
            return self.field_types.NUMBER
        elif type(value) is list:
            return self.field_types.ARRAY
        elif type(value) is dict:
            return self.field_types.OBJECT

    def get_mapper_by_type(self, type: FieldTypeChoices):
        if type is self.field_types.OBJECT:
            return ObjectFieldMapper(self.repository)
        elif type is self.field_types.ARRAY:
            return ListFieldMapper(self.repository)
        elif type is self.field_types.NUMBER:
            return NumberFieldMapper(self.repository)
        elif type is self.field_types.STRING:
            return StringFieldMapper(self.repository)

    def get_mapper_by_value(self, value: Any):
        if self._get_type(value) is self.field_types.OBJECT:
            return ObjectFieldMapper(self.repository)
        elif self._get_type(value) is self.field_types.ARRAY:
            return ListFieldMapper(self.repository)
        elif self._get_type(value) is self.field_types.NUMBER:
            return NumberFieldMapper(self.repository)
        elif self._get_type(value) is self.field_types.STRING:
            return StringFieldMapper(self.repository)
