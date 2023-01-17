from typing import Union

from mappers.services.model_field_service import ModelFieldService


class ModelsApi:
    def list(category_id: Union[int, None]):
        return ModelFieldService.list_models(category_id=category_id)

    def get_by_id(id: int):
        return ModelFieldService.get_model_by_id(id=id)
