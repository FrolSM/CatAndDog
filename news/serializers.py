from rest_framework import serializers
from .models import Post, PostMedia


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['id', 'media_type', 'file', 'order', 'uploaded_at']

class PostSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'category', 'author', 'is_published', 'slug', 'media']
        read_only_fields = ('is_published', 'author')
