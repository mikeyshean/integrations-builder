from integrations.api import IntegrationsApi
from mappers.services.json_mapper_factory import JSONMapperFactory
from mappers.services.json_mapper_service import JSONMapperService
from mappers.services.map_service import MapService
from mappers.services.model_field_service import ModelFieldService
from mappers.services.transformer_factory import TransformerFactory
from mappers.services.transformer_service import TransformerService


class JsonMapperApi:
    def __init__(self):
        transformer_service = TransformerService(
            transformer_factory=TransformerFactory()
        )
        map_service = MapService(transformer_service=transformer_service)
        json_mapper_factory = JSONMapperFactory(map_service=map_service)
        self.service = JSONMapperService(
            json_mapper_factory=json_mapper_factory,
            model_field_service=ModelFieldService(),
        )

    def create_model_from_json_payload(
        self, json_dto: dict, model_name: str, endpoint_id: int
    ):
        type_map = self.service.map_to_json_types(json_dto=json_dto)
        model = self.service.create_models_and_fields_from_type_map(
            type_map=type_map, model_name=model_name
        )
        IntegrationsApi.save_endpoint_model(endpoint_id, model_id=model.id)
        return model
