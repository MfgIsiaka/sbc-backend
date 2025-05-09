from django.db import models
from django.contrib.auth.models import User

from departments_api.models import Department
from programs_api.models import Program 

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('The Username field must be set')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)  # Hash the password
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(username, password, **extra_fields)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # Prompt for role if not provided
        role = extra_fields.get('role')
        if not role:
            from django.core.management import call_command
            import getpass
            role = input("Enter role (e.g., admin, principal, teacher, student, hod): ")
            extra_fields['role'] = role

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICES = [
        
        ('student', 'Student'),
        ('hod', 'Head of Department'),
        ('teacher', 'Teacher'),
        ('principal', 'Principal'),
        ('admin', 'admin'),
    ]
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(null=False , max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True)

    # Additional fields for your custom user
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# Create your models here.
class Profile(models.Model):
   
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    yos = models.PositiveIntegerField(verbose_name='Year of Study', null=True, blank=True)
    nida = models.CharField(max_length=14, unique=True)
    phone_number = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"
    
    

