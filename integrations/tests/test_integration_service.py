import pytest
from django.test import TestCase
from core.exceptions.service_exceptions import AlreadyExistsError

from integrations.services.integration_service import IntegrationService
from integrations.factories import CategoryFactory, IntegrationFactory

@pytest.mark.django_db
class TestIntegrationService(TestCase):
    """
    Test suite for Integration Service
    """
    def setUp(self):
        self.category = CategoryFactory()

    def test_create_integration(self):
        name = "Test Integration"
        integration = IntegrationService.create(name=name, category_id=self.category.id)

        assert integration.name == name
        assert integration.category == self.category
    
    def test_create_duplicate_integration_raises_error(self):
        name = "Test Integration"
        IntegrationService.create(name=name, category_id=self.category.id)

        with self.assertRaises(AlreadyExistsError):
            IntegrationService.create(name=name, category_id=self.category.id)
    
    def test_get_by_name_and_category(self):
        integration = IntegrationFactory()
        response = IntegrationService.get_by_name_and_category(name=integration.name, category=integration.category.name)

        assert response.id == integration.id
        assert response.name == integration.name
        assert response.category.id == integration.category.id
    
    def test_get_by_name_and_category_returns_none(self):
        integration = IntegrationFactory(name="real name")
        response = IntegrationService.get_by_name_and_category(name="fake name", category=integration.category.name)

        assert response is None