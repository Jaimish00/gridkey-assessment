from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.StockTransactionView.as_view(), name="stock-transactions"
    )
]