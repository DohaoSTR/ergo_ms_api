from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random

class RandomNumberView(APIView):
    def get(self, request, *args, **kwargs):
        # Генерация случайного числа
        random_number = random.randint(1, 100)  # Вы можете изменить диапазон по вашему усмотрению
        return Response({'random_number': random_number}, status=status.HTTP_200_OK)
