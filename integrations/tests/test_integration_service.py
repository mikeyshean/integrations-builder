import pytest
from django.db.utils import IntegrityError
from django.test import TestCase
from core.exceptions import UnprocessableError

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

        with self.assertRaises(IntegrityError):
            IntegrationService.create(name=name, category_id=self.category.id)
    
    def test_create_with_unknown_category_raises_error(self):
        name = "Test Integration"
        IntegrationService.create(name=name, category_id=self.category.id)

        with self.assertRaises(UnprocessableError):
            IntegrationService.create(name=name, category_id=-1)
    
    def test_get_by_id(self):
        integration = IntegrationFactory()
        response = IntegrationService.get_by_id(id=integration.id)

        assert response.id == integration.id
        assert response.name == integration.name
        assert response.category.id == integration.category.id
    
    def test_get_by_id_returns_none(self):
        response = IntegrationService.get_by_id(id=-1)

        assert response is None