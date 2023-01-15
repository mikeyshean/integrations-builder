from integrations.services.endpoint_service import EndpointService
from integrations.services.integration_service import IntegrationService


class IntegrationsApi:
    """
    This API class is nothing more than a Pass through at the moment.

    TODO: We will handle any service specific exceptions here that we
    do not want to expose and convert our outputs from all API classes
    to be DTOs or some other primitive.

    The objective being for Services to handle fetching/mutating
    objects and APIs to expose service functionality while return
    a DTO to the caller (View, event handler, etc.)
    """

    @staticmethod
    def create_integration(name: str, category_id: int, domain: str):
        return IntegrationService.create(
            name=name, category_id=category_id, domain=domain
        )

    @staticmethod
    def get_integration_by_id(id: int):
        return IntegrationService.get_by_id(id=id)

    @staticmethod
    def list_integrations():
        return IntegrationService.list_integrations()

    @staticmethod
    def update(
        id: int,
        name: str,
        category_id: int,
        domain_id: int,
        domain: str,
    ):
        return IntegrationService.update(
            id=id,
            name=name,
            category_id=category_id,
            domain_id=domain_id,
            domain=domain,
        )

    @staticmethod
    def delete_integration_by_id(id: int):
        return IntegrationService.delete_integration(id)

    @staticmethod
    def list_categories():
        return IntegrationService.list_categories()

    @staticmethod
    def list_endpoints():
        return EndpointService.list_endpoints()

    @staticmethod
    def get_endpoint_by_id(id: int):
        return EndpointService.get_by_id(id=id)

    @staticmethod
    def create_endpoint(method: str, path: str, integration_id: int):
        return EndpointService.create(
            method=method, path=path, integration_id=integration_id
        )

    @staticmethod
    def delete_endpoint_by_id(id: int):
        return EndpointService.delete_endpoint(id)

    @staticmethod
    def save_endpoint_model(id: int, model_id: int):
        EndpointService.update(id=id, model_id=model_id)

    @staticmethod
    def list_endpoint_models():
        return EndpointService.list_models()

    @staticmethod
    def update_endpoint(id: int, path: str, method: str, integration_id: int):
        EndpointService.update(
            id=id, method=method, path=path, integration_id=integration_id
        )
