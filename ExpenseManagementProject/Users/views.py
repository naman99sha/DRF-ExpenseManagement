from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from ..Users.serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt
import datetime
from django.conf import settings

class registerView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class loginView(APIView):
    def post(self, request):
        email = request.data["email"]
        pw = request.data["password"]

        userObj = get_object_or_404(User, email=email) or None
        if userObj is None:
            raise AuthenticationFailed("User Not Found")
        if not userObj.check_password(pw):
            raise AuthenticationFailed("Incorrect Password")
        
        payload = {
            'id': userObj.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, settings.API_SECRET, alogrithm = 'HS256')
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt":token}
        return Response
    
class userView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        try:
            payload = jwt.decode(
                token, settings.API_SECRET, algorithms = ['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
        
        userObj = get_object_or_404(User, id=payload["id"]) or None
        serializer = UserSerializer(userObj)
        return Response(serializer.data)

class logoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message":"success"
        }
        return response