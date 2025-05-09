from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser, Profile


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
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['yos', 'nida', 'phone_number', 'department', 'program']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, allow_null=True)

    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(), message="Username already exists.")
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(), message="Email already exists.")
        ]
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password', 'profile', 'department']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
        

    def validate_username(self, value):
        cleaned_username = value.strip()
        if CustomUser.objects.filter(username=cleaned_username).exists():
            raise serializers.ValidationError("Username already exists.")
        return cleaned_username

    def validate_email(self, value):
        cleaned_email = value.lower().strip()
        if CustomUser.objects.filter(email=cleaned_email).exists():
            raise serializers.ValidationError("Email already exists.")
        return cleaned_email

    def create(self, validated_data):  
        profile_data = validated_data.pop('profile', None)

        raw_password = validated_data.pop('password')

        validated_data['username'] = validated_data['username'].strip()
        validated_data['email'] = validated_data['email'].strip().lower()

        user = CustomUser.objects.create(**validated_data)
        user.set_password(raw_password)
        user.save()

        if profile_data:
            Profile.objects.create(user=user, **profile_data)

        return user



