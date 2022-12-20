from django.db import transaction

from mappers.field_mappers.factory import FieldMapperFactory
from mappers.models import Field, FieldTypeChoices, Model


class MapperService:
    def __init__(self, field_mapper_factory: FieldMapperFactory):
        self.field_mapper_factory = field_mapper_factory

    def map_to_target_dto(self, remote_dto: dict, remote_model_id: str) -> dict:
        """Maps a known remote dto to it's target dto representation

        Args:
            remote_dto (dict): Remote dto payload
            remote_model_id (str): Known model_id for this dto

        Returns:
            dict: Target dto representation
        """
        field_mapper = self.field_mapper_factory.get_mapper_by_field_value(remote_dto)
        field_mapper.set_remote_model_id(remote_model_id)
        return field_mapper.map_to_target(source_field_value=remote_dto)

    def map_to_types(self, remote_dto: dict) -> dict:
        """Maps an example model to its type structure, similar to JSON Schema

        Args:
            remote_dto (dict): example model data

        Returns:
            dict: Dictionary with field names and type data
        """
        field_mapper = self.field_mapper_factory.get_mapper_by_value(remote_dto)
        return field_mapper.map_to_type(source_value=remote_dto)

    def create_models_and_fields_from_type_map(
        self, type_map: dict, target: bool, model_name: str = "Root"
    ) -> Model:
        """Creates models and fields from a type_map dictionary

        Args:
            type_map (dict): Dictionary with field names and type data
            target (bool): Saves as target model when set to True, \
                otherwise Remote model
            model_name (str, optional): Can be overriden to save a \
                custom model name. Defaults to "Root".

        Returns:
            Model: Instance of a Model
        """
        with transaction.atomic():
            model = Model.objects.create(name=model_name)
            for field_name, type_map in type_map["properties"].items():
                field = self._create_field_from_type_map(field_name, type_map, target)
                field.model = model
                field.save()
        return model

    def _create_field_from_type_map(self, field_name, type_map, target):
        type = type_map["type"]
        field = Field(name=field_name, type=type)

        if type is FieldTypeChoices.ARRAY:
            self._set_array_fields(field_name, type_map, target, field)
        elif type is FieldTypeChoices.OBJECT:
            self._set_object_fields(field_name, type_map, target, field)

        return field

    def _set_object_fields(self, model_name, type_map, target, field):
        field.object_model = self.create_models_and_fields_from_type_map(
            model_name=model_name, type_map=type_map, target=target
        )
        return field

    def _set_array_fields(self, field_name, type_map, target, field):
        item_type = type_map["items"]["type"]
        field.list_item_type = item_type

        if item_type is FieldTypeChoices.OBJECT:
            object_model_name = field_name + "_item"
            self._set_object_fields(
                object_model_name,
                type_map=type_map["items"],
                target=target,
                field=field,
            )
        return field
