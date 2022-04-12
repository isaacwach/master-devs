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

#model class to create new projects 
class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    project_title = models.CharField(max_length=100, null=True)
    project_image = models.ImageField(upload_to='projects/',null=True)
    description = models.TextField(max_length=1000,  null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    tags=models.ManyToManyField(tags, blank=True)
    location=models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    like = models.PositiveIntegerField(default=0)
    
    def __str__(self):
            return self.project_title
    
    def save_image(self):
        self.save()

    #method to querry all project objects and return individual projects   
    @classmethod
    def get_projects(cls):
        projects = Project.objects.all()
        return projects
    
    @classmethod
    def find_project(cls,search_term):
        project = Project.objects.filter(project_title__icontains=search_term)
        return project
    
    @property
    def number_of_comments(self):
        return Comment.objects.filter(project=self).count()
    
    @property
    def number_of_tags(self):
        return tags.objects.filter(project=self).count()
    
    def design(self):
        avg_design =list( map(lambda x: x.design_rating, self.ratings.all()))
        return np.mean(avg_design)

    def usability(self):
        avg_usability =list( map(lambda x: x.usability_rating, self.ratings.all()))
        return np.mean(avg_usability)

    def content(self):
        avg_content =list( map(lambda x: x.content_rating, self.ratings.all()))
        return np.mean(avg_content)

#model class to add comments
class Comment(models.Model):
    content = models.TextField(null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_comment')        
    
    def __str__(self):
        return self.comment
    
    def save_comment(self):
        self.save()    

 #model class to define projectys ratings.The rating ranges between 1 and 10       
class Ratings(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings',null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    design_rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)
    content_rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)
    usability_rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    # def __str__(self):
    #     return self.author        
    
    def save_comment(self):
            self.save()

    def get_comment(self, id):
        comments = Ratings.objects.filter(project_id =id)
        return comments
    
    #method to query all ratings
    @classmethod
    def get_ratings(cls):
        ratings = Ratings.objects.all()
        return rating

class NewsLetterRecipients(models.Model):
    email = models.EmailField(blank=True, null=True)