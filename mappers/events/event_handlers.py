import json

from mappers.services.json_mapper_factory import JSONMapperFactory
from mappers.services.json_mapper_service import JSONMapperService
from mappers.services.map_service import MapService
from mappers.services.model_field_service import ModelFieldService
from mappers.services.transformer_factory import TransformerFactory
from mappers.services.transformer_service import TransformerService


class MapperEventHandlers:
    @staticmethod
    def map_to_target_handler(event: dict):
        transformer_service = TransformerService(
            transformer_factory=TransformerFactory()
        )
        json_mapper_factory = JSONMapperFactory(
            map_service=MapService(transformer_service=transformer_service)
        )
        json_mapper_service = JSONMapperService(
            json_mapper_factory=json_mapper_factory,
            model_field_service=ModelFieldService(),
        )
        dto = json_mapper_service.map_to_target_dto(
            source_dto=event["data"],
            source_model_id=event["source_model_id"],
            map_id=event["map_id"],
        )

        print(f"Pushed MappedEvent to SQS:\n{json.dumps(dto, indent=4)}")
        return dto

    @staticmethod
    def map_to_json_types_handler(event: dict):
        transformer_service = TransformerService(
            transformer_factory=TransformerFactory()
        )
        json_mapper_factory = JSONMapperFactory(
            map_service=MapService(transformer_service=transformer_service)
        )
        json_mapper_service = JSONMapperService(
            json_mapper_factory=json_mapper_factory,
            model_field_service=ModelFieldService(),
        )
        dto = json_mapper_service.map_to_json_types(json_dto=event["data"])

        print(f"Generated Types:\n{json.dumps(dto, indent=4)}")
        return dto
