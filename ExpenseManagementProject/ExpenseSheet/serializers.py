from rest_framework import serializers
from .models import *

class ExpenseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseUserData
        fields = ["userObj","bankBalance","bankName"]

class ExpenseEntry(serializers.ModelSerializer):
    class Meta:
        model = ExpenseEntry
        fields = "__all__"