import pytest
from django.test import TestCase

from mappers.events.event_handlers import MapperEventHandlers
from mappers.models import Map, Model, Transformer, TransformerTypeChoices
from mappers.services.json_mapper_factory import JSONMapperFactory
from mappers.services.json_mapper_service import JSONMapperService
from mappers.services.map_service import MapService
from mappers.services.model_field_service import ModelFieldService
from mappers.services.transformer_factory import TransformerFactory
from mappers.services.transformer_service import TransformerService


@pytest.mark.django_db
class TestMapperEventHandlers(TestCase):
    """
    Test suite for Mapper Events
    """

    def setUp(self):
        transformer_service = TransformerService(
            transformer_factory=TransformerFactory()
        )
        self.map_service = MapService(transformer_service=transformer_service)
        json_mapper_factory = JSONMapperFactory(map_service=self.map_service)
        self.json_mapper_service = JSONMapperService(
            json_mapper_factory=json_mapper_factory,
            model_field_service=ModelFieldService(),
        )

        self._create_target_model()
        self._create_source_model()
        self._create_transformers()

        self.map = self.map_service.create_map(self.source_model, self.target_model)
        self._create_source_to_target_mappings(
            self.source_model, self.target_model, self.map
        )
        self.event = {
            "data": {
                "id": 123456,
                "first_name": "Mike",
                "last_name": "Shean",
                "date_of_birth": "1990-11-10T00:00:00Z",
                "gender": "MALE",
                "skills": [
                    {"id": "s1", "name": "Sweeping"},
                    {"id": "s2", "name": "Typing"},
                ],
                "jobs": ["Cleaning", "Programming"],
                "address": {"id": "a1", "street": "123 Road"},
            },
            "sync_id": "sync-id",
            "source_model_id": self.source_model.id,
            "map_id": self.map.id,
        }

    def test_map_to_target_event(self):
        response = MapperEventHandlers.map_to_target_handler(self.event)
        expected_response = {
            "target_id": 123456,
            "target_first_name": "MIKE",  # Transformed field
            "target_last_name": "Shean",
            "target_date_of_birth": "1990-11-10T00:00:00Z",
            "target_skills": [
                {"target_id": "s1", "target_name": "Sweeping"},
                {"target_id": "s2", "target_name": "Typing"},
            ],
            "target_jobs": ["Cleaning", "Programming"],
            "target_address": {"target_id": "a1", "target_street": "123 Road"},
            "target_gender": "MALE",
        }

        assert response == expected_response

    def test_map_to_types_event(self):
        response = MapperEventHandlers.map_to_json_types_handler(self.event)
        expected_response = {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "date_of_birth": {"type": "string"},
                "gender": {"type": "string"},
                "skills": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                        },
                    },
                },
                "jobs": {"type": "array", "items": {"type": "string"}},
                "address": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "street": {"type": "string"},
                    },
                },
            },
        }

        assert response == expected_response

    def _create_target_model(self):
        target_data = {
            "target_id": 123456,
            "target_first_name": "Mike",
            "target_last_name": "Shean",
            "target_date_of_birth": "1990-11-10T00:00:00Z",
            "target_gender": "MALE",
            "target_skills": [
                {"target_id": "s1", "target_name": "Sweeping"},
                {"target_id": "s2", "target_name": "Typing"},
            ],
            "target_jobs": ["Cleaning", "Programming"],
            "target_address": {"target_id": "a1", "target_street": "123 Road"},
        }

        type_map = self.json_mapper_service.map_to_json_types(json_dto=target_data)
        self.target_model = (
            self.json_mapper_service.create_models_and_fields_from_type_map(type_map)
        )

    def _create_source_model(self):
        data = {
            "id": 123456,
            "first_name": "Mike",
            "last_name": "Shean",
            "date_of_birth": "1990-11-10T00:00:00Z",
            "gender": "MALE",
            "skills": [
                {"id": "s1", "name": "Sweeping"},
                {"id": "s2", "name": "Typing"},
            ],
            "jobs": ["Cleaning", "Programming"],
            "address": {"id": "a1", "street": "123 Road"},
        }
        type_map = self.json_mapper_service.map_to_json_types(json_dto=data)
        self.source_model = (
            self.json_mapper_service.create_models_and_fields_from_type_map(
                type_map=type_map
            )
        )

    def _create_transformers(self):
        self.transformer = Transformer.objects.create(
            type=TransformerTypeChoices.UPPERCASE
        )

    def _create_source_to_target_mappings(
        self, source_model: Model, target_model: Model, map: Map
    ):
        self.map_service.create_model_map(
            source_model=source_model, target_model=target_model, map=map
        )
        for source_field in source_model.fields.all():
            target_field_name = "target_" + source_field.name
            target_field = target_model.fields.get(name=target_field_name)

            field_map = self.map_service.create_field_map(
                source_field=source_field, target_field=target_field, map=map
            )

            if source_field.name == "first_name":
                field_map.transformer = self.transformer
                field_map.save()

            if source_field.object_model_id:
                self._create_source_to_target_mappings(
                    source_field.object_model, target_field.object_model, map=map
                )
