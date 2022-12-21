from django.db import transaction

from mappers.models import Field, FieldTypeChoices, Model
from mappers.services.json_mapper.factory import JSONMapperFactory
from mappers.services.model_field_service import ModelFieldService


class JSONMapperService:
    def __init__(
        self,
        field_mapper_factory: JSONMapperFactory,
        model_field_service: ModelFieldService,
    ):
        self.field_mapper_factory = field_mapper_factory
        self.field_mapper_factory.add_service(model_field_service)
        self.model_field_service = model_field_service

    def map_to_target_dto(self, remote_dto: dict, remote_model_id: str) -> dict:
        """Maps a known remote dto to it's target dto representation

        Args:
            remote_dto (dict): Remote dto payload
            remote_model_id (str): Known model_id for this dto

        Returns:
            dict: Target dto representation
        """
        field_mapper = self.field_mapper_factory.get_mapper_by_value(remote_dto)
        field_mapper.set_remote_model_id(remote_model_id)
        return field_mapper.map_to_target(remote_value=remote_dto)

    def map_to_json_types(self, json_dto: dict) -> dict:
        """Maps an example model to its type structure, similar to JSON Schema

        Args:
            remote_dto (dict): example model data

        Returns:
            dict: Dictionary with field names and type data
        """
        field_mapper = self.field_mapper_factory.get_mapper_by_value(json_dto)
        return field_mapper.map_to_json_type(dto=json_dto)

    @transaction.atomic
    def create_models_and_fields_from_type_map(
        self, type_map: dict, is_remote: bool, model_name: str = "Root"
    ) -> Model:
        """Creates models and fields from a type_map dictionary

        Args:
            type_map (dict): Dictionary with field names and type data
            is_remote (bool): Saves as Remote model when set to True by \
                setting is_remote flag, otherwise Target model
            model_name (str, optional): Can be overriden to save a \
                custom model name. Defaults to "Root".

        Returns:
            Model: Instance of a Model
        """
        model = self.model_field_service.create_model(
            name=model_name, is_remote=is_remote
        )
        for field_name, field_type_map in type_map["properties"].items():
            field = self._create_field_from_type_map(
                model.id, field_name, field_type_map, is_remote
            )
            field.model = model
            field.save()
        return model

    def _create_field_from_type_map(
        self, model_id, field_name, type_map, is_remote
    ) -> Field:
        type = self._get_field_type_from_json_type(type_map["type"])
        field = self.model_field_service.create_field(
            name=field_name, type=type, model_id=model_id
        )

        if type is FieldTypeChoices.ARRAY:
            field = self._update_array_field(field_name, type_map, field.id, is_remote)
        elif type is FieldTypeChoices.OBJECT:
            field = self._update_object_field(field_name, type_map, field.id, is_remote)

        return field

    def _update_object_field(self, model_name, type_map, field_id, is_remote) -> Field:
        object_model = self.create_models_and_fields_from_type_map(
            model_name=model_name, is_remote=is_remote, type_map=type_map
        )
        return self.model_field_service.update_field(
            field_id=field_id, object_model_id=object_model.id, is_remote=is_remote
        )

    def _update_array_field(self, field_name, type_map, field_id, is_remote) -> Field:
        item_type = self._get_field_type_from_json_type(type_map["items"]["type"])
        field = self.model_field_service.update_field(
            field_id=field_id, list_item_type=item_type, is_remote=is_remote
        )

        if item_type is FieldTypeChoices.OBJECT:
            object_model_name = field_name + "_item"
            field = self._update_object_field(
                model_name=object_model_name,
                type_map=type_map["items"],
                field_id=field.id,
                is_remote=is_remote,
            )
        return field

    def _get_field_type_from_json_type(self, type: str) -> FieldTypeChoices:
        return FieldTypeChoices[type.upper()]
