from core.exceptions import NotFoundError
from integrations.services.endpoint_service import EndpointService
from integrations.services.integration_service import IntegrationService


class IntegrationsApi:
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
    def save_endpoint_model(endpoint_id: int, model_id: int):
        endpoint = EndpointService.get_by_id(id=endpoint_id)
        if not endpoint:
            raise NotFoundError("Endpoint not found")

        EndpointService.save_model(endpoint, model_id)

    @staticmethod
    def list_endpoint_models():
        return EndpointService.list_models()
