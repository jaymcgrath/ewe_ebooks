from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    """
    one to one related to contrib.auth.User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    offline_name = models.CharField(max_length=88, null=True, blank=True)
    email = models.EmailField()
    bio = models.TextField(null=True, blank=True)
    dob = models.DateField(auto_now=False)
    last_active = models.DateTimeField(auto_now=True)
    #
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance, **kwargs)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

    def __str__(self):
        return self.offline_name

    def __repr__(self):
        return self.offline_name

