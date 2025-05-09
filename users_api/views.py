from django.shortcuts import render
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Or customize based on your need
    

class RegisterUserView(APIView):
    def post(self, request):
        print("Received data:", request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateUserView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # URL will use /update/users/<id>/

    def update(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        instance = self.get_object()

        # Validate uniqueness of username and email (excluding current user)
        username = request.data.get('username')
        email = request.data.get('email')

        if username and CustomUser.objects.filter(username=username).exclude(id=user_id).exists():
            return Response({'username': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if email and CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            return Response({'email': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with the normal update
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)