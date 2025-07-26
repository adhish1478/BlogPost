from django.urls import path, include
from .views import RegisterView, register_page
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
urlpatterns=[
    path('api/register/', RegisterView.as_view(), name= 'register-api'),
    path('api/token/', TokenObtainPairView.as_view(), name= 'token'),
    path('api/refresh/', TokenRefreshView.as_view(), name= 'token-refresh'),
    path('api/logout/', TokenBlacklistView.as_view(), name= 'logout'),
    # render html urls
    path('register/', register_page, name='register-page'),
]