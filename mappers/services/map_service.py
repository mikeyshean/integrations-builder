from typing import Any

from mappers.exceptions import NotFoundError
from mappers.models import Field, FieldMap, Mapper, Model, ModelMap, Transformer
from mappers.services.transformer_service import TransformerService


class MapService:
    def __init__(self, transformer_service: TransformerService):
        self.transformer_service = transformer_service

    @staticmethod
    def create_map(source_model: Model, target_model: Model):
        """
        Creates root Map instance with associated source and target Models

        Args:
            source_model (Model): Model we are are mapping from
            target_model (Model): Model we are mapping to

        Returns:
            (Map): Instance of the Map object
        """
        return Mapper.objects.create(
            source_model=source_model, target_model=target_model
        )

    @staticmethod
    def get_map_by_id(id: int):
        return Mapper.objects.filter(id=id).first()

    @staticmethod
    def create_model_map(source_model: Model, target_model: Model, map: Mapper):
        """
        Create sub-mappings for nested models.

        Args:
            source_model (Model): Nested model we are mapping from
            target_model (Model): Model we are mapping to
            map (Map): The root Map for this nested source_model

        Returns:
            (ModleMap): Instance of ModelMap
        """
        return ModelMap.objects.create(
            source_model=source_model, target_model=target_model, map=map
        )

    @staticmethod
    def create_field_map(
        source_field: Field,
        target_field: Field,
        map: Mapper,
        transformer: Transformer = None,
    ):
        """
        Create field to field mappings via FieldMap instance

        Args:
            source_field (Field): Field we are mapping from
            target_field (Field): Field we are mapping to
            map (Map): The root Map for this nested source_model
            transformer (Transformer): Transformer to be applied during mapping

        Returns:
            (FieldMap): Instance of FieldMap
        """

        return FieldMap.objects.create(
            source_field=source_field,
            target_field=target_field,
            map=map,
            transformer=transformer,
        )

    @staticmethod
    def get_target_field(source_field: Field, map_id: int) -> Field:
        field_map = FieldMap.objects.filter(
            source_field=source_field, map_id=map_id
        ).first()
        if not field_map:
            raise NotFoundError(
                f"FieldMap not found for source field: {source_field}, map_id: {map_id}"
            )
        return field_map.target_field

    def transform(self, source_field: Field, map_id: int, source_value: Any):
        field_map = FieldMap.objects.filter(
            source_field=source_field, map_id=map_id
        ).first()
        if not field_map:
            raise NotFoundError(
                f"FieldMap not found for source field: {source_field}, map_id: {map_id}"
            )
        transformer = field_map.transformer

        return (
            self.transformer_service.transform(transformer, source_value)
            if transformer
            else source_value
        )
