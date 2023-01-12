from mappers.services.model_field_service import ModelFieldService


class ModelsApi:
    def list():
        return ModelFieldService.list_models()
