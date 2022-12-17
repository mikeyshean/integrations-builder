from rest_framework import serializers
from integrations.models import Integration

class IntegrationSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id', allow_null=False)

    class Meta:
        model = Integration
        fields = ('id', 'name', 'category_id')