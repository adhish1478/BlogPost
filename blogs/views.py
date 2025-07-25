from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
# Create your views here.

class PostViewSet(ModelViewSet):
    queryset= Post.objects.all().order_by('-created_at')
    serializer_class= PostSerializer
    permission_classes= [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author= self.request.user)

    @action(detail= True, methods= ['POST'], permission_classes= [IsAuthenticated])
    def toggle_like(self, request, pk= None):
        post= self.get_object()
        user= request.user

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response({'likes count': post.likes.count()})
    
    @action(detail=True, methods=['GET'])
    def likes(self, request, pk=None):
        post = self.get_object()
        users = post.likes.all()
        return Response([
            {"id": user.id, "username": user.username, "email": user.email}
            for user in users
        ])
    

class CommentViewSet(ModelViewSet):
    serializer_class= CommentSerializer
    permission_classes= [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id= self.kwargs['post_pk'])
    
    def perform_create(self, serializer):
        serializer.save(author= self.request.user, post_id= self.kwargs['post_pk'])