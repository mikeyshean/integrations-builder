from integrations.models import Integration, Category
from core.exceptions import UnprocessableError

class IntegrationService:

    @staticmethod
    def create(name: str, category_id: int) -> Integration:
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise UnprocessableError(message="Invalid category")
        return Integration.objects.create(name=name, category=category)
    
    @staticmethod
    def get_by_id(id: int) -> Integration:
        return Integration.objects.filter(id=id).first()
