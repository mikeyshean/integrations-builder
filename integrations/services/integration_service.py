import logging
from typing import List

from core.exceptions import NotFoundError, UnprocessableError
from integrations.models import Category, Domain, Integration

logger = logging.getLogger(__name__)


class IntegrationService:
    @staticmethod
    def create(name: str, category_id: int, domain: str) -> Integration:
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise UnprocessableError(message="Invalid category")

        integration = Integration.objects.create(name=name, category=category)

        if domain and integration:
            Domain.objects.create(domain=domain, integration=integration)

        return integration

    @staticmethod
    def get_by_id(id: int) -> Integration:
        return Integration.objects.filter(id=id).first()

    @staticmethod
    def list_integrations() -> List[Integration]:
        return (
            Integration.objects.all()
            .select_related("category")
            .prefetch_related("endpoints")
            .prefetch_related("domains")
        )

    @staticmethod
    def list_categories() -> List[Category]:
        return Category.objects.all()

    @staticmethod
    def delete_integration(id: int) -> bool:
        try:
            Integration.objects.get(id=id).delete()
        except Integration.DoesNotExist:
            raise NotFoundError()
