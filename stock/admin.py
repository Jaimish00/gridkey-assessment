from django.contrib.admin import register, ModelAdmin
from .models import StockTransaction


@register(StockTransaction)
class StockTransactionAdmin(ModelAdmin):
    """Custom admin for StockTransaction"""

    list_display = [
        "id",
        "trade_type",
        "trade_date",
        "price",
        "quantity",
        "split_ratio",
        "balance_quantity",
        "average_buy_price"
    ]
