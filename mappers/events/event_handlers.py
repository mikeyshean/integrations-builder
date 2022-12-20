import json

from mappers.field_mappers.factory import FieldMapperFactory
from mappers.repository import MappingRepository
from mappers.service import MapperService


class MapperEventHandlers:
    @staticmethod
    def map_to_target_handler(event: dict):
        field_mapper_factory = FieldMapperFactory(MappingRepository())
        mapper_service = MapperService(field_mapper_factory)
        dto = mapper_service.map_to_target_dto(
            remote_dto=event["data"], remote_model_id=event["remote_model_id"]
        )

        print(f"Pushed MappedEvent to SQS:\n{json.dumps(dto, indent=4)}")
        return dto

    @staticmethod
    def map_to_types_handler(event: dict):
        field_mapper_factory = FieldMapperFactory(MappingRepository())
        mapper_service = MapperService(field_mapper_factory)
        dto = mapper_service.map_to_types(remote_dto=event["data"])

        print(f"Generated Types:\n{json.dumps(dto, indent=4)}")
        return dto
