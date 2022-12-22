from typing import Any

from mappers.field_transformers import FieldTransformerFactory
from mappers.models import Transformer


class TransformerService:
    def __init__(self, transformer_factory: FieldTransformerFactory):
        self._transformer_factory = transformer_factory

    def get_transformer_by_id(self, id: int) -> Transformer:
        return Transformer.objects.filter(id=id).first()

    def transform(self, transformer: Transformer, value: Any) -> Any:
        field_transformer = self._transformer_factory.get_transformer_by_type(
            transformer.type
        )
        return field_transformer.transform(value)
