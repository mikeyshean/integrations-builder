from rest_framework import serializers

from mappers.models import Field, Model


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ("id", "name", "type")


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
