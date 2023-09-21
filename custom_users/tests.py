from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import customuser,Verification
from django.utils import timezone
from rest_framework.authtoken.models import Token



class RegisterUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_success(self):
        url = reverse('register') 
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'privacy_security': True
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_failure(self):
        url = reverse('register')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'password': 'insecure',  
            'privacy_security': True
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = customuser.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='securepassword',
            privacy_security=True
        )

    def test_user_login_success(self):
        url = reverse('login')
        data = {
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_failure(self):
        url = reverse('login')
        data = {
            'email': 'jane.doe@example.com',  
            'password': 'wrongpassword'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

class UserLogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = customuser.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='securepassword',
            privacy_security=True
        )
        self.token = Token.objects.create(user=self.user)

    def test_user_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('logout')

        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

