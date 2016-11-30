from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    """
    one to one related to contrib.auth.User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    offline_name = models.CharField(max_length=88, null=True, blank=True)
    email = models.EmailField()
    bio = models.TextField(null=True, blank=True)
    dob = models.DateTimeField(auto_now=False)
    last_active = models.DateTimeField(auto_now=True)


