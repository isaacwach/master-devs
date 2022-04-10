from django.contrib import admin

#import all model classes from models import
from .models import Profile, Project, Location, tags, Comment, Ratings


admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(tags)
admin.site.register(Ratings)
