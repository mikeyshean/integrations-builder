from mappers.exceptions import NotFoundError
from mappers.models import Field, FieldTypeChoices, Model


class ModelFieldService:
    def create_model(
        self,
        *,
        name: str = "",
    ) -> Model:
        obj = Model(name=name)
        obj.full_clean()
        obj.save()
        return obj

    def create_field(
        self,
        *,
        model_id: int,
        name: str = "",
        type: FieldTypeChoices = FieldTypeChoices.UNKNOWN,
    ) -> Field:
        obj = Field(model_id=model_id, name=name, type=type)
        obj.full_clean()
        obj.save()
        return obj

    def update_field(self, *, field_id: int, **kwargs) -> Field:
        field = Field.objects.filter(id=field_id).first()
        if not field:
            raise NotFoundError("Field could not be found for update")

        valid_fields = Field.get_update_fields()
        update_fields = []
        for key, value in kwargs.items():
            if key in valid_fields:
                update_fields.append(key)
                setattr(field, key, value)

        field.full_clean()
        field.save(update_fields=update_fields)
        return field

    def get_model_by_id(self, model_id: int) -> Field:
        return Model.objects.filter(id=model_id).first()

    def get_field_by_id(self, field_id: int) -> Field:
        return Field.objects.filter(id=field_id).first()

    def get_fields_by_model_id(self, model_id: int):
        model = self.get_model_by_id(model_id)
        if not model:
            raise NotFoundError("Model could not be found")
        return list(model.fields.all())

    def get_target_field_from_remote_field_id(self, remote_field_id: int) -> Field:
        field = (
            Field.objects.filter(id=remote_field_id)
            .select_related("target_field")
            .first()
        )
        return field.target_field if field else None
