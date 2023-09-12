from django.core import validators
from django.db import models

from .constants import SPLIT_RATIO_REGEX
from .text_choices import TradeTypeChoices
from djmoney.models.fields import MoneyField


class StockTransaction(models.Model):
    trade_type = models.CharField(choices=TradeTypeChoices.choices, max_length=10)
    quantity = models.IntegerField(help_text="Number of shares traded")
    trade_date = models.DateField()
    price = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency="INR",
        help_text="Price per share"
    )
    split_ratio = models.CharField(
        validators=[validators.RegexValidator(
            SPLIT_RATIO_REGEX
        )],
        blank=True,
        null=True,
        default=None,
        max_length=10,
        help_text="Split ratio of the stock"
    )

    balance_quantity = models.IntegerField(null=True, blank=True, default=None)
    average_buy_price = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency="INR",
        help_text="Average buy price",
        null=True,
        blank=True,
        default=None
    )
