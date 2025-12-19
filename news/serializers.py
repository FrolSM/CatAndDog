from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'author', 'time', 'title', 'text', 'category', 'photo', 'video', 'is_published', 'slug')
        read_only_fields = ('is_published', 'author')
