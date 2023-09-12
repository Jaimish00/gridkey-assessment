# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StockTransaction
from .text_choices import TradeTypeChoices


@receiver(post_save, sender=StockTransaction)
def update_balance_and_average_buy_price(sender, instance, created, **kwargs):
    if created:
        # * Get the related transactions ordered by trade_date
        transactions = StockTransaction.objects.filter(
            trade_date__lte=instance.trade_date
        ).order_by("trade_date", "id")

        list_of_buy_trades = []

        # * Iterate over each transaction
        for transaction in transactions:
            # * If it's a buy, just append
            if transaction.trade_type == TradeTypeChoices.BUY:
                list_of_buy_trades.append([transaction.quantity, transaction.price])
            # * If it's a sell, use FIFO approach to start selling stocks from first buy
            elif transaction.trade_type == TradeTypeChoices.SELL:
                sell_quantity = transaction.quantity
                buy_index = 0
                while sell_quantity > 0:
                    if len(list_of_buy_trades) <= buy_index:
                        raise ValueError("You don't have enough stocks to sell")

                    if list_of_buy_trades[buy_index][0] >= sell_quantity:
                        if list_of_buy_trades[buy_index][0] - sell_quantity >= 0:
                            list_of_buy_trades[buy_index][0] -= sell_quantity
                            break

                    sell_quantity -= list_of_buy_trades[buy_index][0]
                    list_of_buy_trades[buy_index][0] = 0
                    buy_index += 1

        instance.balance_quantity = sum([sublist[0] for sublist in list_of_buy_trades])
        instance.average_buy_price = (
            sum([sublist[0] * sublist[1] for sublist in list_of_buy_trades])
            / instance.balance_quantity
        )
