from rest_framework import serializers

from integrations.models import Category, Domain, Endpoint, Integration


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class BasicIntegrationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Integration
        fields = ("id", "name", "category")


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ("id", "domain")


class ListIntegrationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    endpoint_count = serializers.ReadOnlyField(source="endpoints.count")
    domains = DomainSerializer(many=True)

    class Meta:
        model = Integration
        fields = ("id", "name", "category", "endpoint_count", "domains")


class CreateIntegrationSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    domain = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        fields = ("name", "category_id", "domain")


class CreateEndpointSerializer(serializers.Serializer):
    method = serializers.CharField()
    path = serializers.CharField()

    class Meta:
        fields = ("method", "path")


class ModelSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        fields = ("id", "name")


class EndpointSerializer(serializers.ModelSerializer):
    integration = BasicIntegrationSerializer()
    model = ModelSerializer()

    class Meta:
        model = Endpoint
        fields = ("id", "method", "path", "integration", "model")
