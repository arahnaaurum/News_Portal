from .models import *
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['id', 'type', 'time_creation', 'title', 'text', 'rating',]
