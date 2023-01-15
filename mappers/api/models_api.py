from mappers.services.model_field_service import ModelFieldService


class ModelsApi:
    def list():
        return ModelFieldService.list_models()

    def get_by_id(id: int):
        return ModelFieldService.get_model_by_id(id=id)
