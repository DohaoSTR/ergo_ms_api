from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.management import call_command
from io import StringIO
from .models import BitcoinPrice
from .serializers import BitcoinPriceSerializer
from rest_framework import generics


class BitcoinPriceListAPIView(generics.ListAPIView):
    queryset = BitcoinPrice.objects.all().order_by('-timestamp')  # [:100]
    serializer_class = BitcoinPriceSerializer


class ExecuteCommandAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            days = request.data.get("days", 10)
            out = StringIO()
            call_command('fetch_price', days=days, stdout=out)
            return Response({'status': 'success', 'output': out.getvalue()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


