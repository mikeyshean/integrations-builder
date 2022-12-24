import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.exceptions import UnprocessableError
from integrations.api import IntegrationsApi
from integrations.serializers import IntegrationSerializer

logger = logging.getLogger(__name__)


class IntegrationsViewSet(ViewSet):

    permission_classes = (IsAuthenticated,)

    def create(self, request):
        try:
            serializer = IntegrationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            integration = IntegrationsApi.create_integration(
                name=data["name"], category_id=data["category"]["id"]
            )
            response_serializer = IntegrationSerializer(integration)
            return Response(response_serializer.data)
        except UnprocessableError as e:
            return Response(e.message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def retrieve(self, request, pk):
        integration = IntegrationsApi.get_integration_by_id(id=pk)
        if not integration:
            return Response("Integration not found", status=status.HTTP_404_NOT_FOUND)

        serializer = IntegrationSerializer(integration)
        return Response(serializer.data)

    def list(self, request):
        integrations = IntegrationsApi.list_integrations()

        serializer = IntegrationSerializer(integrations, many=True)
        return Response(serializer.data)
