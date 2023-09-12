from django.db import models
from django.utils.translation import gettext_lazy as _


class TradeTypeChoices(models.TextChoices):
    BUY = "buy", _("BUY")
    SELL = "sell", _("SELL")
    SPLIT = "split", _("SPLIT")
    