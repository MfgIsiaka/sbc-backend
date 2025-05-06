from django.db import models


from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=255)
    hod = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_hod')
   

    def __str__(self):
        return self.name
