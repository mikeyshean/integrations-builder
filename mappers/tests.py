import pytest
from django.test import TestCase

from mappers.events.event_handlers import MapperEventHandlers


@pytest.mark.django_db
class TestMapperEventHandlers(TestCase):
    """
    Test suite for Mapper Events
    """

    def setUp(self):
        self.event = {
            "data": {
                "id": "123456",
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
            "remote_model_id": "m1",
        }

    def test_map_to_target_event(self):

        response = MapperEventHandlers.map_to_target_handler(self.event)
        expected_response = {
            "target_id": "123456",
            "target_first_name": "Mike",
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
        response = MapperEventHandlers.map_to_types_handler(self.event)
        expected_response = {
            "type": "OBJECT",
            "properties": {
                "id": {"type": "STRING"},
                "first_name": {"type": "STRING"},
                "last_name": {"type": "STRING"},
                "date_of_birth": {"type": "STRING"},
                "gender": {"type": "STRING"},
                "skills": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "id": {"type": "STRING"},
                            "name": {"type": "STRING"},
                        },
                    },
                },
                "jobs": {"type": "ARRAY", "items": {"type": "STRING"}},
                "address": {
                    "type": "OBJECT",
                    "properties": {
                        "id": {"type": "STRING"},
                        "street": {"type": "STRING"},
                    },
                },
            },
        }

        assert response == expected_response
