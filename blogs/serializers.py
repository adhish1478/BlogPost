from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    author= serializers.ReadOnlyField(source= 'author.username')
    likes_count= serializers.SerializerMethodField()
    is_liked= serializers.SerializerMethodField()

    class Meta:
        model= Post
        fields= ['id', 'title', 'content', 'author', 'updated_at', 'likes_count', 'is_liked', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        user= self.context['request'].user
        return user.is_authenticated and user in obj.likes.all()
    
class CommentSerializer(serializers.ModelSerializer):
    author= serializers.ReadOnlyField(source= 'author.username')

    class Meta:
        model= Comment
        fields= ['id', 'post', 'author', 'text', 'created_at']
        read_only_fields = ['author', 'post', 'created_at']