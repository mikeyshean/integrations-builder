import logging
from typing import List

from core.exceptions import NotFoundError, UnprocessableError
from integrations.models import Endpoint, Integration

logger = logging.getLogger(__name__)


class EndpointService:
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
            Endpoint.objects.all().select_related("integration").select_related("model")
        )

    @staticmethod
    def delete_endpoint(id: int) -> bool:
        try:
            Endpoint.objects.get(id=id).delete()
        except Endpoint.DoesNotExist:
            raise NotFoundError()