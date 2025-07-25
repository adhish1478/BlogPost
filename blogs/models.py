from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title= models.CharField(max_length=250, null= False)
    content= models.TextField(null= False)
    author= models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'posts')
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post= models.ForeignKey(Post, on_delete= models.CASCADE, related_name= 'comments')
    author= models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'comments')
    text= models.TextField(null= False)
    created_at= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"comment by {self.author.username} on {self.post.title}: {self.text}"
