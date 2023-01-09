from rest_framework import serializers

from integrations.models import Category, Integration


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class IntegrationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Integration
        fields = ("id", "name", "category")
