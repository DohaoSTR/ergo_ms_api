from rest_framework.response import Response
from rest_framework import status
from src.core.utils.base.base_views import BaseAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from src.external.tools.generator.methods import generate_random_list

class GenerateListView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Получение информации о пользователе.",
        manual_parameters=[
            openapi.Parameter(
                'start',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="Начало диапазона",
                default=1,
            ),
            openapi.Parameter(
                'end',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="Начало диапазона",
                default=10,
            ),
            openapi.Parameter(
                'count',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="Начало диапазона",
                default=10,
            ),
        ],
        responses={
            200: "Успешно создан лист",
            400: "Неправильные параметры при запросе",
        }
    )
    def get(self, request):
        try:
            start = int(request.query_params.get('start', 1))
            end = int(request.query_params.get('end', 10))
            count = int(request.query_params.get('count', 10))

            random_list = generate_random_list(start, end, count)

            return Response(
                {
                    "data": random_list,
                    "message": "Список чисел успешно создан"
                },
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )