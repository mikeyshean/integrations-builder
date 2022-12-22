from typing import Any

from mappers.exceptions import NotFoundError
from mappers.models import Field, FieldMap, Map, Model, ModelMap, Transformer
from mappers.services.transformer_service import TransformerService


class MapService:
    def __init__(self, transformer_service: TransformerService):
        self.transformer_service = transformer_service

    @staticmethod
    def create_map(source_model: Model, target_model: Model):
        return Map.objects.create(source_model=source_model, target_model=target_model)

    @staticmethod
    def get_map_by_id(id: int):
        return Map.objects.filter(id=id).first()

    @staticmethod
    def create_model_map(source_model: Model, target_model: Model, map: Map):
        return ModelMap.objects.create(
            source_model=source_model, target_model=target_model, map=map
        )

    @staticmethod
    def create_field_map(
        source_field: Field,
        target_field: Field,
        map: Map,
        transformer: Transformer = None,
    ):
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
