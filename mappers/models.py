from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimestampedModel


class Model(TimestampedModel):
    name = models.CharField(max_length=64, help_text="Name of the model")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id: {self.id}, name: {self.name})"


class Mapper(TimestampedModel):
    source_model = models.ForeignKey(
        "Model", on_delete=models.CASCADE, related_name="+", null=False
    )
    target_model = models.ForeignKey(
        "Model", on_delete=models.CASCADE, related_name="+", null=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_model", "target_model"], name="unique_source_and_target"
            )
        ]


class TransformerTypeChoices(models.TextChoices):
    UPPERCASE = "UPPERCASE", _("Uppercase")
    LOWERCASE = "LOWERCASE", _("Lowercase")
    CAPITALIZE = "CAPITALIZE", _("Captalize")
    STRING_TO_FLOAT = "STRING_TO_FLOAT", _("String to Float")
    STRING_TO_INTEGER = "STRING_TO_INTEGER", _("String to Integer")
    STRING_TO_BOOLEAN = "STRING_TO_BOOLEAN", _("String to Boolean")
    NUMBER_TO_STRING = "NUMBER_TO_STRING", _("Number to String")


class Transformer(TimestampedModel):
    type = models.CharField(
        max_length=64,
        choices=TransformerTypeChoices.choices,
        null=False,
        help_text="Name of the transformer type",
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(type: {self.type})"


class FieldTypeChoices(models.TextChoices):
    OBJECT = "OBJECT", _("Object")
    LIST = "LIST", _("List")
    STRING = "STRING", _("String")
    NUMBER = "NUMBER", _("Number")
    BOOLEAN = "BOOLEAN", _("Boolean")
    UNKNOWN = "UNKNOWN", _("Unknown")


class Field(TimestampedModel):
    name = models.CharField(max_length=64, help_text="Name of the field")
    type = models.CharField(
        max_length=32,
        choices=FieldTypeChoices.choices,
        help_text="Name of the field type",
    )
    choices = models.JSONField(
        null=True, blank=True, help_text="List of enum choices for this field"
    )
    list_item_type = models.CharField(
        max_length=32,
        choices=FieldTypeChoices.choices,
        null=True,
        blank=True,
        help_text="Name of list item's type",
    )
    object_model = models.ForeignKey(
        "Model",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
        help_text="Reference to a model if this field's value is another model",
    )
    model = models.ForeignKey(
        "Model",
        on_delete=models.CASCADE,
        related_name="fields",
        null=False,
        blank=False,
        help_text="Reference to the model that this field belongs to",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["model", "name"], name="unique_model_and_field_name"
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_type_valid",
                check=models.Q(type__in=FieldTypeChoices.values),
            ),
        ]

    @staticmethod
    def get_update_fields():
        return ["name", "type", "list_item_type", "object_model_id", "target_field_id"]

    def get_type(self) -> FieldTypeChoices:
        return FieldTypeChoices[self.type]

    def get_list_item_type(self) -> FieldTypeChoices:
        return FieldTypeChoices[self.list_item_type]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id: {self.id}, name: {self.name})"


class ModelMap(TimestampedModel):
    source_model = models.ForeignKey(
        "Model", on_delete=models.CASCADE, related_name="+", null=False
    )
    target_model = models.ForeignKey(
        "Model", on_delete=models.CASCADE, related_name="+", null=False
    )
    mapper = models.ForeignKey(
        "Mapper", on_delete=models.CASCADE, related_name="+", null=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_model", "mapper", "target_model"],
                name="%(app_label)s_%(class)s_unique_source_mapper_target",
            )
        ]


class FieldMap(TimestampedModel):
    source_field = models.ForeignKey(
        "Field", on_delete=models.CASCADE, related_name="+", null=False
    )
    target_field = models.ForeignKey(
        "Field", on_delete=models.CASCADE, related_name="+", null=False
    )
    mapper = models.ForeignKey(
        "Mapper", on_delete=models.CASCADE, related_name="+", null=False
    )
    transformer = models.ForeignKey(
        "Transformer", on_delete=models.CASCADE, related_name="+", null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_field", "mapper", "target_field"],
                name="%(app_label)s_%(class)s_unique_source_mapper_target",
            )
        ]
