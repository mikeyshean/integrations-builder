from rest_framework import serializers

from integrations.models import Category, Endpoint, Integration


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ("id", "name")


class BasicIntegrationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Integration
        fields = ("id", "name", "category")


class ListIntegrationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    endpoint_count = serializers.ReadOnlyField(source="endpoints.count")

    class Meta:
        model = Integration
        fields = ("id", "name", "category", "endpoint_count")


class CreateIntegrationSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        model = Integration
        fields = ("name", "category_id")
