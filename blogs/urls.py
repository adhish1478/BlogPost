from rest_framework_nested import routers
from django.urls import path
from .views import PostViewSet, CommentViewSet, display_dash

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

posts_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

api_urlpatterns = router.urls + posts_router.urls

html_urlpatterns= [
    path('dashboard/', display_dash, name='dashboard'),
]