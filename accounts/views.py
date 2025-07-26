from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
# Create your views here.

class RegisterView(CreateAPIView):
    queryset= User.objects.all()
    serializer_class= RegisterSerializer

def register_page(request):
    return render(request, 'accounts/register.html')

def login_page(request):
    return render(request, 'accounts/login.html')