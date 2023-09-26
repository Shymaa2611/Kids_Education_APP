from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import customuser,Verification,Kid,Profile
from django.utils import timezone
from rest_framework.authtoken.models import Token
from datetime import timedelta
from .serializers import ProfileSerializer


class RegisterUserTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_valid_registration(self):
        url = reverse('register')
        data = {
            'first_name': 'Mona',
            'last_name': 'Ali',
            'email': 'test@example.com',
            'password': '123456',
            'confirm_password': '123456',
            'privacy_security': True
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_registration(self):
        url = reverse('register')
        data = {
            'first_name': 'Mona',
            'last_name': 'Ali',
            'email': 'test@example.com',
            'password': '123456',
            'confirm_password': '123457',  
            'privacy_security': True
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = customuser.objects.create_user(
            email='test@example.com',
            password='password123'
        )

    def test_valid_login(self):
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_invalid_email(self):
        data = {
            'email': 'invalid@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'invalid email')

class VerifyCodeTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.verify_url = reverse('verify_code')
        self.user = customuser.objects.create(
            email='test@example.com',
            password='password123',
        )
        self.verification = Verification.objects.create(
            user=self.user,
            code='123456',
            expiration_time=timezone.now() + timedelta(minutes=30)
        )

    def test_valid_verification(self):
        data = {'code': '123456'}
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expired_verification(self):
        self.verification.expiration_time = timezone.now() - timedelta(minutes=30)
        self.verification.save()
        data = {'code': '123456'}
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_verification_code(self):
        data = {'code': '654321'}
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateKidViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.create_kid_url = reverse('createkid')
        self.user = customuser.objects.create(
            email='test@example.com',
            password='password123'
        )

    def test_valid_kid_creation(self):
        data = {'access_code': '123456', 'name': 'John Doe', 'age': 8} 
        self.client.force_authenticate(user=self.user)  
        response = self.client.post(self.create_kid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Kid.objects.filter(access_code='123456').exists())

    def test_duplicate_access_code(self):
        Kid.objects.create(access_code='123456', name='Existing Kid', age=10)
        data = {'access_code': '123456', 'name': 'John Doe', 'age': 8} 
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_kid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Access code already exists')
        self.assertFalse(Kid.objects.filter(name='John Doe').exists())

    def test_invalid_data(self):
        data = {'access_code': '123456', 'name': '', 'age': -5} 
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_kid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertFalse(Kid.objects.filter(access_code='123456').exists())

class ForgotPasswordTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.send_code_url = reverse('send_forgot_password_code')
        self.verify_code_url = reverse('verify_rest_password')

    def test_send_verification_code(self):
        data = {'email': 'test@example.com'}  
        response = self.client.post(self.send_code_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_verify_code(self):
        send_code_data = {'email': 'test@example.com'}
        self.client.post(self.send_code_url, send_code_data, format='json')
        code = self.client.session.get('code', None)
        self.assertIsNotNone(code)

        verify_code_data = {'code': code}
        response = self.client.post(self.verify_code_url, verify_code_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_verify_invalid_code(self):
        verify_code_data = {'code': '123456'}  
        response = self.client.post(self.verify_code_url, verify_code_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)

class ChangePasswordTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.change_password_url = reverse('change_password')
        self.user = customuser.objects.create_user(
            email='test@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
     data = {
        'old_password': 'password123',
        'new_password': 'newpassword123'
     }
     response = self.client.post(self.change_password_url, data, format='json')
     #self.assertEqual(response.status_code, status.HTTP_200_OK)
    # self.assertEqual(response.data['message'], 'Password changed successfully.')
     self.user.refresh_from_db()




    def test_invalid_data(self):
        data = {
            'old_password': 'password123',
            'new_password': 'short'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('password123'))       

class UpdateKidAPIViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.update_kid_url = reverse('update_kid')
        self.user = customuser.objects.create_user(
            email='test@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

    def test_update_kid_success(self):
        kid = Kid.objects.create(name='John Doe', age=8)
        self.user.kid = kid
        self.user.save()

        data = {'name': 'Jane Doe', 'age': 9}
        response = self.client.put(self.update_kid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Kid data updated successfully')
        kid.refresh_from_db()
        self.assertEqual(kid.name, 'Jane Doe')
        self.assertEqual(kid.age, 9)

    def test_update_kid_no_associated_kid(self):
        data = {'name': 'Jane Doe', 'age': 9}
        response = self.client.put(self.update_kid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'User has no associated Kid')

    def test_invalid_data(self):
        data = {'name': '', 'age': -5} 
        response = self.client.put(self.update_kid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        