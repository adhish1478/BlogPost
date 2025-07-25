from django.contrib import admin
from .models import Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'

    def liked_by(self, obj):
        return ", ".join([user.username for user in obj.likes.all()])
    liked_by.short_description = 'Liked By'

    list_display= ('title', 'author__username', 'likes_count', 'created_at')
    search_fields= ('author__username',)
    list_filter= ('created_at', 'updated_at')
    
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display= ('post__title', 'author__username', 'text')
    search_fields= ('author__username', 'post__title',)
    list_filter= ('created_at', 'post__title')
admin.site.register(Comment, CommentAdmin)