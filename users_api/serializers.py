from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser, Profile
from departments_api.models import Department
from programs_api.models import Program

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['username'] = user.username
        token['email'] = user.email
        token['id'] = user.id
        token['role'] = user.role
        # If you have roles/groups
        # token['role'] = user.groups.first().name if user.groups.exists() else 'user'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
        }
        
        return data



# USER SERIALIZER

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id','user', 'yos', 'nida', 'phone_number', 'department', 'program', 'image']



