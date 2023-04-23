from django.urls import path
from .views import *

urlpatterns = [
    path("add-balance",addBankBalance.as_view(),name="addBalance"),
]