from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
class CustomUser(User):
    contact = models.CharField(max_length=20)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20)
"""
