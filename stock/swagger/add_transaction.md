### Add transaction 

## Choices
1. buy
2. sell
3. split


#### Sample request in case of buy and sell
```
{
    "trade_type": "sell",
    "price": "45",
    "quantity": 100000,
    "trade_date": "2018-02-18"
}
```

---

#### Sample request in case of split
```
{
    "trade_type": "split",
    "split_ratio": "1:15"
    "trade_date": "2018-02-18"
}
```

---

#### Success response
```
{
    "id": 49,
    "trade_type": "sell",
    "price": "45.0000",
    "quantity": 100000,
    "trade_date": "2018-02-18",
    "split_ratio": null,
    "balance_quantity": 1165000,
    "average_buy_price": "4.0909",
    "average_buy_price_currency": "INR"
}
```
``HTTP 201``

---

### Failure, if stock quantity is not enough for sell
```
{
    "message": "You don't have enough stocks to sell"
}
```
``HTTP 400``
