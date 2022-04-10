from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','user','image','bio','contact')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Project
        fields =('id','project_title','date_posted', 'description','project_link')  