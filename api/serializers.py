from rest_framework import serializers
from django.contrib.auth.models import User
from  .models import userProfile

class UserSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username',read_only=True)
    email=serializers.EmailField(source='user.email',read_only=True)
    first_name=serializers.CharField(source="user.first_name",read_only=True)
    last_name=serializers.CharField(source="user.last_name",read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)

    class Meta:
        model = userProfile
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'role_id',
            'token_id',
            'date_created',
            'date_modified',
            'activated_at',
        )