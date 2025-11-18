from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from api.models import userProfile
from api.serializers import UserSerializer,CreateUserSerialzer,UpdateUserSerializer

class CreateUserAPI(generics.CreateAPIView):
    queryset=userProfile.objects.all()
    serializer_class=CreateUserSerialzer
    permission_classes=(AllowAny)

class UpdateUserAPI(generics.UpdateAPIView):
    queryset=userProfile.objects.all()
    serializer_class=UpdateUserSerializer
