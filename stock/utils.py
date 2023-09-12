import os


def find_balance_quantity_and_avg_buy_price(list_of_buy_trades):
    """
    Find balance quantity and Average buy price

    Parameters:
        list_of_buy_trades(list): List of Buy trades

    Returns:
        Balance quantity, average buy price
    """

    balance_quantity = sum([sublist[0] for sublist in list_of_buy_trades])
    avg_buy_price = (
        sum([sublist[0] * sublist[1] for sublist in list_of_buy_trades])
        / balance_quantity
    )
    return balance_quantity, avg_buy_price


def get_swagger_description(description_file_path):
    """
    Read swagger description markdown

    Parameters:
        description_file_path(str): File path

    Returns:
        swagger description file content

    Raises:
        Exception
    """

    if not os.path.isfile(description_file_path):
        raise Exception("Swagger description file not found")

    with open(description_file_path, "r") as file:
        data = file.read()
        return data
