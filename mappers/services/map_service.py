from mappers.models import Field, FieldMap, Map, Model, ModelMap, Transformer


class MapService:
    @staticmethod
    def create_map(source_model: Model, target_model: Model):
        return Map.objects.create(source_model=source_model, target_model=target_model)

    @staticmethod
    def get_map_by_id(id: int):
        return Map.objects.filter(id=id).first()

    @staticmethod
    def create_model_map(source_model: Model, target_model: Model, map: Map):
        return ModelMap.objects.create(
            source_model=source_model, target_model=target_model, map=map
        )

    @staticmethod
    def create_field_map(
        source_field: Field,
        target_field: Field,
        map: Map,
        transformer: Transformer = None,
    ):
        return FieldMap.objects.create(
            source_field=source_field,
            target_field=target_field,
            map=map,
            transformer=transformer,
        )
