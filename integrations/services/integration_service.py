import logging
from typing import List

from core.exceptions import NotFoundError, UnprocessableError
from integrations.models import Category, Domain, Integration

logger = logging.getLogger(__name__)


class IntegrationService:
    UPDATABLE_FIELDS = ["category_id", "name", "domain", "domain_id"]

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
    def update(id: int, **kwargs):
        try:
            integration = Integration.objects.get(id=id)
        except Integration.DoesNotExist:
            raise NotFoundError("Integration not found")

        domain_name = None
        domain_id = None
        update_fields = []
        for field, value in kwargs.items():
            # TODO: Clean up this nasty custom handling in here for an
            # assumed single domain once we do allow multiple domains
            # per integration from client
            if field == "domain":
                domain_name = value
                continue
            if field == "domain_id":
                domain_id = value
                continue

            if field in IntegrationService.UPDATABLE_FIELDS:

                setattr(integration, field, value)
                update_fields.append(field)

        if domain_name and domain_id:
            try:
                domain = integration.domains.get(id=domain_id)
                domain.domain = domain_name
                domain.save(update_fields=["domain"])
            except Domain.DoesNotExist:
                raise NotFoundError("Domain not found")

        integration.save(update_fields=update_fields)

    @staticmethod
    def list_categories() -> List[Category]:
        return Category.objects.all()

    @staticmethod
    def delete_integration(id: int) -> bool:
        try:
            Integration.objects.get(id=id).delete()
        except Integration.DoesNotExist:
            raise NotFoundError()
