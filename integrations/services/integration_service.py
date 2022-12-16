from django.core.exceptions import ValidationError
from integrations.models import Integration
from django.db import IntegrityError
from core.exceptions.service_exceptions import AlreadyExistsError

class IntegrationService:

    @staticmethod
    def create(name: str, category_id: int) -> Integration:
        try:
            return Integration.objects.create(name=name, category_id=category_id)
        except IntegrityError:
            raise AlreadyExistsError(message=f"Integration already exists with this name: {name}")
    
    @staticmethod
    def get_by_name_and_category(name: str, category: str) -> Integration:
        return Integration.objects.filter(name=name, category__name=category).first()

