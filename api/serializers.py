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


class CreateUserSerialzer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)                                                               
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password'                                                      
            ]
        extra_kwargs={
        'password':{'write_only':True}
        }

def validate(self,attrs):
            if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError({"email":"Email already exists"})
            if User.objects.filter(username=attrs['username']).exists():
                raise serializers.ValidationError({'username':'Username has been taken'})
            return attrs
        
def create(self,validated_data):
            user=User(
                username=validated_data['username'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user