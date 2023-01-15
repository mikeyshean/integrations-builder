import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.exceptions import UnprocessableError
from mappers.api.json_mapper_api import JsonMapperApi
from mappers.api.models_api import ModelsApi
from mappers.serializers import CreateModelFromPayload, ModelSerializer

logger = logging.getLogger(__name__)


class JsonMapperViewSet(ViewSet):

    permission_classes = (IsAuthenticated,)
    api = JsonMapperApi()

    @action(
        detail=False,
        methods=["post"],
        url_path="model-from-payload",
        name="Create model from JSON payload",
    )
    def model_from_payload(self, request):
        try:
            serializer = CreateModelFromPayload(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            model = self.api.create_model_from_json_payload(
                json_dto=data["json"],
                model_name=data["model_name"],
                endpoint_id=data["endpoint_id"],
            )
            response_serializer = ModelSerializer(model)
            return Response(response_serializer.data)
        except UnprocessableError as e:
            return Response(e.message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ValidationError as e:
            errors = {}
            for k, v in e.detail.items():
                errors[k] = map(lambda detail: detail.title(), v)
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ModelViewSet(ViewSet):

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        models = ModelsApi.list()
        serializer = ModelSerializer(models, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk: int):
        model = ModelsApi.get_by_id(id=pk)
        serializer = ModelSerializer(model)
        return Response(serializer.data)
