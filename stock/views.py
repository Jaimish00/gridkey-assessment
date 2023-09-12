from dateutil.parser import parse
from django.db import transaction
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import StockTransaction
from .serializers import StockTransactionSerializer


class StockTransactionView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = StockTransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        try:
            serializer.save()
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": e.args[0]
            })

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def get(self, request):
        trade_date = request.query_params.get("trade_date", "").strip()

        filters = Q()

        try:
            parsed_date = parse(trade_date)
            filters |= Q(trade_date__lte=parsed_date)
        except ValueError:
            pass

        queryset = StockTransaction.objects.filter(filters).order_by('trade_date')

        serializer = StockTransactionSerializer(queryset, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)
