from rest_framework import serializers
from django.contrib.auth.models import User
from  ..Models.user_models import userProfile
from  django.contrib.auth import authenticate
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
            'password',
            'first_name',
            'last_name'
            ]
        extra_kwargs={
        'password':{'write_only':True,
                    'required':True}
        }

    def validate(self,attrs):
            if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError({"email":"Email already exists"})
            if User.objects.filter(username=attrs['username']).exists():
                raise serializers.ValidationError({'username':'Username has been taken'})
            return attrs
        
    def create(self,validated_data):
           password=validated_data.pop('password')
           user=User.objects.create(**validated_data)
           user.set_password(password)
           user.save()
           return user

           ###########update user serializer#################
class UpdateUserSerializer(serializers.ModelSerializer):
     username = serializers.CharField(source='user.username', required=False)
     email = serializers.EmailField(source='user.email', required=False)
     first_name = serializers.CharField(source='user.first_name', required=False)
     last_name = serializers.CharField(source='user.last_name', required=False)

     class Meta:
        model = userProfile
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            
        ]

       
     def update(self,instance,validated_data):
         #extracting the  user data from the validated data
         user_data=validated_data.pop('user',{})
        #update user
         user=instance.user
         for attr,value in user_data.items():
             setattr(user,attr,value)
         user.save()
         #update userprofile
         for attr,value in validated_data.items():
             setattr(instance,attr,value)
         instance.save()
         return instance
     
        ###########login user serializer#################

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username does not exist.")

        # Authenticate the user
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Incorrect username or password.")

        attrs['user'] = user
        return attrs
