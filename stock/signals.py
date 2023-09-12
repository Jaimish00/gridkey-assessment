from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StockTransaction
from .text_choices import TradeTypeChoices
from .utils import find_balance_quantity_and_avg_buy_price


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
                        # * If a buy suffices the sell amount, just deduct and break
                        if list_of_buy_trades[buy_index][0] - sell_quantity >= 0:
                            list_of_buy_trades[buy_index][0] -= sell_quantity
                            break

                    sell_quantity -= list_of_buy_trades[buy_index][0]
                    list_of_buy_trades[buy_index][0] = 0
                    buy_index += 1
            elif transaction.trade_type == TradeTypeChoices.SPLIT:
                split_amount = int(transaction.split_ratio.split(":")[1])

                list_of_buy_trades = [
                    [list_of_buy_trade[0] * split_amount, list_of_buy_trade[1] / split_amount]
                    for list_of_buy_trade in list_of_buy_trades
                ]

        balance_quantity, avg_buy_price = find_balance_quantity_and_avg_buy_price(
            list_of_buy_trades
        )
        instance.balance_quantity = balance_quantity
        instance.average_buy_price = avg_buy_price

        instance.save()
