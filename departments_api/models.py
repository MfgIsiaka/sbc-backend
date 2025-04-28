from django.db import models

from colleges_api.models import College
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=255)
    hod = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_hod')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name
