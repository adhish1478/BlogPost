from django.urls import path, include
from .views import RegisterView, MeView, register_page, login_page
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
    path('api/me/', MeView.as_view(), name='me-api'),
    # render html urls
    path('register/', register_page, name='register-page'),
    path('login/', login_page, name='login-page'),
]