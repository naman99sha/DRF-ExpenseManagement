from django.shortcuts import render, get_object_or_404
from .serializers import ExpenseEntrySerializer, ExpenseUserSerializer
from .models import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework import status
import jwt
from django.conf import settings
from Users.models import User
from datetime import date

class addBankBalance(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated, Please Login first")
        
        try:
            payload = jwt.decode(
                token, settings.API_SECRET, algorithms = ['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated, Please Login Again")
        
        userObj = get_object_or_404(User, id=payload["id"]) or None
        if not userObj:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        bankUserObj = get_object_or_404(ExpenseUserData, userObj=userObj) or None
        if bankUserObj:
            try:
                amount = float(request.data["amount"])
            except:
                return Response({"message":"Either amount is not passed, or an invalid amount passed. Amount should be numeric"}, status=status.HTTP_400_BAD_REQUEST)
            bankUserObj.bankBalance += amount
            bankUserObj.save()
            expenseEntryObj = ExpenseEntry(userObj=bankUserObj,title="Amount Credited by User",transactionType="Credit",date=date.today(),amount = amount)
            expenseEntryObj.save()
            bankUserSerializer = ExpenseUserSerializer(bankUserObj)
            return Response(bankUserSerializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":"Bank details for this user does not exist"},status=status.HTTP_404_NOT_FOUND)

class addExpenseEntry(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated, Please Login first")
        
        try:
            payload = jwt.decode(
                token, settings.API_SECRET, algorithms = ['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated, Please Login Again")
        
        userObj = get_object_or_404(User, id=payload["id"]) or None
        if not userObj:
            return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        bankUserObj = get_object_or_404(ExpenseUserData, userObj=userObj) or None
        if bankUserObj:
            expenseEntryObj = ExpenseEntry(userObj=bankUserObj,title=request.data["title"],transactionType=request.data["transactionType"],date=date.today(),amount = request.data["amount"])
            expenseEntryObj.save()
            if request.data["transactionType"] == "Credit":
                bankUserObj.bankBalance += request.data["amount"]
            else:
                bankUserObj.bankBalance -= request.data["amount"]
            bankUserObj.save()
            bankUserSerializer = ExpenseUserSerializer(bankUserObj)
            return Response(bankUserSerializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":"Bank details for this user does not exist"},status=status.HTTP_404_NOT_FOUND)