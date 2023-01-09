from integrations.services.integration_service import IntegrationService


class IntegrationsApi:
    @staticmethod
    def create_integration(name: str, category_id: int):
        return IntegrationService.create(name=name, category_id=category_id)

    @staticmethod
    def get_integration_by_id(id: int):
        return IntegrationService.get_by_id(id=id)

    @staticmethod
    def list_integrations():
        return IntegrationService.list_integrations()

    @staticmethod
    def list_categories():
        return IntegrationService.list_categories()
