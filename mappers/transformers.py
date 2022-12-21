from abc import ABC, abstractmethod
from typing import Union

from mappers.models import TransformerTypeChoices


class FieldTransformer(ABC):
    @abstractmethod
    def transform(self, value: Union[str, int, float]) -> Union[str, int, float]:
        pass


class UppercaseTransformer(FieldTransformer):
    def transform(self, value: Union[str, int, float]):
        return value.upper()


class StringToFloatTransformer(FieldTransformer):
    def transform(self, value: Union[str, int, float]):
        return float(value)


class FieldTransformerFactory:

    TRANSFORMER_MAP = {
        TransformerTypeChoices.UPPERCASE: UppercaseTransformer(),
        TransformerTypeChoices.STRING_TO_FLOAT: StringToFloatTransformer(),
    }

    def get_transformer_by_type(self, type: TransformerTypeChoices) -> FieldTransformer:
        return self.TRANSFORMER_MAP[type]
