import json

from mappers.json_mappers import JSONMapperFactory
from mappers.services.json_mapper_service import JSONMapperService
from mappers.services.model_field_service import ModelFieldService
from mappers.services.transformer_service import TransformerService
from mappers.transformers import FieldTransformerFactory


class MapperEventHandlers:
    @staticmethod
    def map_to_target_handler(event: dict):
        transformer_service = TransformerService(
            transformer_factory=FieldTransformerFactory()
        )
        field_mapper_factory = JSONMapperFactory(
            transformer_service=transformer_service
        )
        json_mapper_service = JSONMapperService(
            field_mapper_factory, ModelFieldService()
        )
        dto = json_mapper_service.map_to_target_dto(
            remote_dto=event["data"], remote_model_id=event["remote_model_id"]
        )

        print(f"Pushed MappedEvent to SQS:\n{json.dumps(dto, indent=4)}")
        return dto

    @staticmethod
    def map_to_json_types_handler(event: dict):
        transformer_service = TransformerService(
            transformer_factory=FieldTransformerFactory()
        )
        field_mapper_factory = JSONMapperFactory(
            transformer_service=transformer_service
        )
        json_mapper_service = JSONMapperService(
            field_mapper_factory, ModelFieldService()
        )
        dto = json_mapper_service.map_to_json_types(json_dto=event["data"])

        print(f"Generated Types:\n{json.dumps(dto, indent=4)}")
        return dto
