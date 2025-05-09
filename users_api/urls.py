# users_api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import RegisterUserView
from .views import UpdateUserView


router = DefaultRouter()
router.register(r'', UserViewSet)  # You can also use 'register(r'users', ...)' here

urlpatterns = [
    path('users/', include(router.urls)),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('update/users/<int:id>/', UpdateUserView.as_view(), name='update-user'),
    
]




