from django.db import models
from django.contrib.auth.models import User

from colleges_api.models import College
from departments_api.models import Department
from programs_api.models import Program 

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('hod', 'Head of Department'),
        ('teacher', 'Teacher'),
        ('principal', 'Principal'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    yos = models.PositiveIntegerField(verbose_name='Year of Study', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    nida = models.CharField(max_length=14, unique=True)
    phone_number = models.CharField(max_length=10)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"