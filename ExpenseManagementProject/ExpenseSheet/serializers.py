from rest_framework import serializers
from .models import *

class ExpenseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseUserData
        fields = ["userObj","bankBalance","bankName"]

class ExpenseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseEntry
        fields = ["title","transactionType","date","amount"]