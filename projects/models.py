from django.db import models
from PIL import Image
from django.contrib.auth.models import User
import numpy as np
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator

# A prifile class to create and save user profiles 
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    contact=models.IntegerField(default=0)
    bio = models.TextField(max_length=100)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    #method to save users
    def save_profile(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()

        return profile

#create create_profile receiver function 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

#model to create users location
class Location(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def save_location(self):
        self.save()

    #method to delete a location
    def delete_location(self):
        self.delete()

#Tag class model that inherits from models.Model and creates a tag
class tags(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def save_tags(self):
        self.save()

    def delete_tags(self):
        self.delete()
