from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from .constants import SPLIT_RATIO_REGEX
from .models import StockTransaction
from .text_choices import TradeTypeChoices


class StockTransactionSerializer(serializers.ModelSerializer):
    split_ratio = serializers.RegexField(regex=SPLIT_RATIO_REGEX, required=False)
    trade_type = serializers.ChoiceField(
        choices=TradeTypeChoices.choices, required=True
    )
    price = MoneyField(
        max_digits=19, decimal_places=4, default_currency="INR", required=False
    )
    quantity = serializers.IntegerField(required=False, default=0, allow_null=True)

    def validate(self, data):
        trade_type = data.get("trade_type")
        price = data.get("price")
        quantity = data.get("quantity")
        split_ratio = data.get("split_ratio")

        # * If trade type is BUY or SELL, price and quantity should be there
        if trade_type in [TradeTypeChoices.BUY.value, TradeTypeChoices.SELL.value]:
            if price is None:
                raise serializers.ValidationError(
                    {"price": f"Price is required for trade type {trade_type}"}
                )
            elif quantity is None:
                raise serializers.ValidationError(
                    {"quantity": f"Quantity is required for trade type {trade_type}"}
                )
        # * If trade type is SPLIT, ratio should be there
        elif trade_type == TradeTypeChoices.SPLIT:
            if split_ratio is None:
                raise serializers.ValidationError(
                    {
                        "split_ratio": f"Split ratio is required for trade type {trade_type}"
                    }
                )

        if trade_type in [TradeTypeChoices.BUY.value, TradeTypeChoices.SELL.value]:
            data["split_ratio"] = None
        elif trade_type == TradeTypeChoices.SPLIT:
            data["price"] = 0
            data["quantity"] = 0

        return data

    class Meta:
        model = StockTransaction
        fields = [
            "id",
            "trade_type",
            "price",
            "quantity",
            "trade_date",
            "split_ratio",
            "balance_quantity",
            "average_buy_price",
            "average_buy_price_currency",
        ]
