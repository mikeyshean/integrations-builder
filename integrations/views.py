import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.exceptions import NotFoundError, UnprocessableError
from integrations.api import IntegrationsApi
from integrations.serializers import (
    BasicIntegrationSerializer,
    CategorySerializer,
    CreateEndpointSerializer,
    CreateIntegrationSerializer,
    EndpointSerializer,
    ListIntegrationSerializer,
)

logger = logging.getLogger(__name__)


class IntegrationsViewSet(ViewSet):

    permission_classes = (IsAuthenticated,)

    def create(self, request):
        try:
            serializer = CreateIntegrationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            integration = IntegrationsApi.create_integration(
                name=data["name"],
                category_id=data["category_id"],
                domain=data["domain"],
            )
            response_serializer = BasicIntegrationSerializer(integration)
            return Response(response_serializer.data)
        except UnprocessableError as e:
            return Response(e.message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def retrieve(self, request, pk):
        integration = IntegrationsApi.get_integration_by_id(id=pk)
        if not integration:
            return Response("Integration not found", status=status.HTTP_404_NOT_FOUND)

        serializer = BasicIntegrationSerializer(integration)
        return Response(serializer.data)

    def list(self, request):
        integrations = IntegrationsApi.list_integrations()

        serializer = ListIntegrationSerializer(integrations, many=True)
        return Response(serializer.data)

    def delete(self, request, pk: int):
        try:
            IntegrationsApi.delete_integration_by_id(pk)
            return Response(status=status.HTTP_200_OK)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"], url_path="endpoints")
    def endpoints(self, request, pk=None):
        try:
            serializer = CreateEndpointSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            integration = IntegrationsApi.create_endpoint(
                method=data["method"],
                path=data["path"],
                integration_id=pk,
            )
            response_serializer = EndpointSerializer(integration)
            return Response(response_serializer.data)
        except UnprocessableError as e:
            return Response(e.message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @endpoints.mapping.get
    def get_endpoints(self, request, pk=None):
        integration = IntegrationsApi.get_integration_by_id(id=pk)
        if not integration:
            return Response("Integration not found", status=status.HTTP_404_NOT_FOUND)

        serializer = EndpointSerializer(integration.endpoints, many=True)
        return Response(serializer.data)


class IntegrationCategoriesViewSet(ViewSet):

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        categories = IntegrationsApi.list_categories()

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class EndpointViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        endpoints = IntegrationsApi.list_endpoints()

        serializer = EndpointSerializer(endpoints, many=True)
        return Response(serializer.data)

    def delete(self, request, pk: int):
        try:
            IntegrationsApi.delete_endpoint_by_id(pk)
            return Response(status=status.HTTP_200_OK)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk):
        endpoint = IntegrationsApi.get_endpoint_by_id(id=pk)
        if not endpoint:
            return Response("Endpoint not found", status=status.HTTP_404_NOT_FOUND)

        serializer = EndpointSerializer(endpoint)
        return Response(serializer.data)
