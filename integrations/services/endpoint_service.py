import logging
from typing import List

from core.exceptions import NotFoundError, UnprocessableError
from integrations.models import Endpoint, Integration

logger = logging.getLogger(__name__)


class EndpointService:
    UPDATABLE_FIELDS = ["path", "method", "integration_id", "model_id"]

    @staticmethod
    def create(method: str, path: str, integration_id: int) -> Endpoint:
        integration = Integration.objects.filter(id=integration_id).first()
        if not integration:
            raise UnprocessableError(message="Invalid integration")

        return Endpoint.objects.create(
            method=method, path=path, integration_id=integration_id
        )

    @staticmethod
    def get_by_id(id: int) -> Endpoint:
        return Endpoint.objects.filter(id=id).first()

    @staticmethod
    def list_endpoints() -> List[Endpoint]:
        return (
            Endpoint.objects.all()
            .select_related("integration", "integration__category")
            .select_related("model")
        )

    @staticmethod
    def delete_endpoint(id: int) -> bool:
        try:
            Endpoint.objects.get(id=id).delete()
        except Endpoint.DoesNotExist:
            raise NotFoundError()

    @staticmethod
    def update(id: int, **kwargs):
        endpoint = Endpoint.objects.filter(id=id).first()

        if not endpoint:
            raise NotFoundError("Endpoint not found")

        update_fields = []
        for field, value in kwargs.items():
            if field in EndpointService.UPDATABLE_FIELDS:
                setattr(endpoint, field, value)
                update_fields.append(field)

        endpoint.save(update_fields=update_fields)

        return endpoint

    @staticmethod
    def list_models():
        """
        Fetch list of all Endpoint Models
        """
        return Endpoint.objects.select_related(
            "model", "integration", "integration__category"
        ).filter(model__isnull=False)

    @staticmethod
    def get_models(id: int):
        """
        Fetch list models for a given endpoint id
        """
        return Endpoint.objects.select_related(
            "model", "integration", "integration__category"
        ).filter(id=id)
