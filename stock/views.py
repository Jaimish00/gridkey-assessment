from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockTransactionSerializer


class StockTransactionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StockTransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        serializer.save()

        return Response(status=status.HTTP_200_OK, data=serializer.data)

