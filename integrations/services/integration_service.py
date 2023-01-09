from typing import List

from core.exceptions import UnprocessableError
from integrations.models import Category, Integration


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

    @staticmethod
    def list_integrations() -> List[Integration]:
        return Integration.objects.all()

    @staticmethod
    def list_categories() -> List[Category]:
        return Category.objects.all()
