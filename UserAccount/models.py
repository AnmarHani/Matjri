from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    username = OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    description = models.TextField()
    image = models.ImageField(default="user.png", upload_to="images", blank=True)
    followers = models.ManyToManyField(User, null=True, blank=True)


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)

post_save.connect(create_profile, sender=User)

'''
  def count_like(self):
    return self.likes.count() 
'''