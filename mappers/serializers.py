from rest_framework import serializers

from mappers.models import Field, Model


class ObjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ("id", "name")


class FieldSerializer(serializers.ModelSerializer):
    object_model = ObjectModelSerializer(read_only=True)

    class Meta:
        model = Field
        fields = ("id", "name", "type", "object_model", "list_item_type")


class ModelSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Model
        fields = ("id", "name", "fields")


class CreateModelFromPayload(serializers.Serializer):
    json = serializers.DictField()
    model_name = serializers.CharField()
    endpoint_id = serializers.IntegerField()

    class Meta:
        fields = ("json", "model_name", "endpoint_id")
