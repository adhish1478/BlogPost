from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class AccountsAPITest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register-api')
        self.token_url = reverse('token')
        self.me_url = reverse('me-api')
        self.logout_url = reverse('logout')

        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpass123"
        }

        self.user = User.objects.create_user(**self.user_data)

    # Checks if the user registration endpoint works correctly
    def test_user_registration(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

     # Checks if the user registration fails with duplicate username   
    def test_duplicate_username_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # checks token generation works correctly
    def test_token_generation(self):
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # checks if the user can access their own correct data using their token
    def test_me_view_authenticated(self):
        # login and get token
        token_res = self.client.post(self.token_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        })
        access = token_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_data["username"])
    
    # Ensures the user cannot access their own data without being authenticated
    def test_me_view_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Tests the logout functionality to ensure it blacklists the token
    def test_logout_blacklists_token(self):
        # Get refresh token
        token_res = self.client.post(self.token_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        })
        refresh = token_res.data["refresh"]

        # Blacklist it
        response = self.client.post(self.logout_url, {"refresh": refresh})
        self.assertIn(response.status_code, [status.HTTP_205_RESET_CONTENT, status.HTTP_200_OK])

    # Ensures that a blacklisted token cannot be reused
    def test_reuse_blacklisted_token(self):
        token_res = self.client.post(self.token_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        })
        refresh = token_res.data["refresh"]

        # Blacklist
        self.client.post(self.logout_url, {"refresh": refresh})
        
        # Try using again
        response = self.client.post(reverse("token-refresh"), {"refresh": refresh})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)