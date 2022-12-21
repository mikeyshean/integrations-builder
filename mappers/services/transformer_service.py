from typing import Any

from mappers.exceptions import NotFoundError
from mappers.models import Transformer
from mappers.transformers import FieldTransformerFactory


class TransformerService:
    def __init__(self, transformer_factory: FieldTransformerFactory):
        self._transformer_factory = transformer_factory

    def get_transformer_by_id(self, id: int) -> Transformer:
        return Transformer.objects.filter(id=id).first()

    def transform(self, id: int, value: Any) -> Any:
        transformer = self.get_transformer_by_id(id)
        if not transformer:
            raise NotFoundError("Transformer not found")

        field_transformer = self._transformer_factory.get_transformer_by_type(
            transformer.type
        )
        return field_transformer.transform(value)
