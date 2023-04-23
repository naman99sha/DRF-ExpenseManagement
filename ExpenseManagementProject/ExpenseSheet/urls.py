from django.urls import path
from .views import *

urlpatterns = [
    path("add-balance",addBankBalance.as_view(),name="addBalance"),
    path("add-expense-entry",addExpenseEntry.as_view(),name="addExpenseEntry"),
]