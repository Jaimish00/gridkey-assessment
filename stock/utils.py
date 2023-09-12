def find_balance_quantity_and_avg_buy_price(list_of_buy_trades):
    balance_quantity = sum([sublist[0] for sublist in list_of_buy_trades])
    avg_buy_price = (
        sum([sublist[0] * sublist[1] for sublist in list_of_buy_trades])
        / balance_quantity
    )
    return balance_quantity, avg_buy_price
