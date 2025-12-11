from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,permissions
from rest_framework.permissions import AllowAny
from api.Models.user_models import userProfile
from api.serializers.user_serializers import UserSerializer,CreateUserSerialzer,UpdateUserSerializer,LoginUserSerializer
from knox import views as Knox_view
from django.contrib.auth import login
from django.contrib.auth.models import User

class CreateUserAPI(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=CreateUserSerialzer
    permission_classes=[AllowAny]

class UpdateUserAPI(generics.UpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UpdateUserSerializer


class LoginUserView(Knox_view.LoginView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        # Get Knox token response
        response = super().post(request, format)
        # Get user profile
        try:
            profile = userProfile.objects.get(user=user)
            user_data = UserSerializer(profile).data
        except userProfile.DoesNotExist:
            user_data = {"id": user.id}
        # Build custom response
        response.data["user"] = user_data
        return response


class DeleteAccountAPI(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user