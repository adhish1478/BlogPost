from rest_framework_nested import routers
from django.urls import path
from .views import PostViewSet, CommentViewSet, display_home, post_detail_view

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

posts_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

api_urlpatterns = router.urls + posts_router.urls

html_urlpatterns= [
    path('', display_home, name='home'),
    path('posts/<int:post_id>/', post_detail_view, name='post-detail-view'),
]