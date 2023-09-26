from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from .models import Category,Challenge
from custom_users.models import customuser,Kid
from .views import create_3_equations

class CategoriesAPITest(TestCase):

    def setUp(self):
        Category.objects.create(category_title='Category 1')
        Category.objects.create(category_title='Category 2')

    def test_get_categories(self):
        url = reverse('get_categories') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ChallengeAPITest(TestCase):

    def setUp(self):
        category = Category.objects.create(category_title='Category 1')
        Challenge.objects.create(title='Challenge 1', category=category)
        Challenge.objects.create(title='Challenge 2', category=category)

    def test_get_challenge(self):
        url = reverse('get_Challenge')  
        category_title = 'Category 1'
        response = self.client.get(url, data={'category': category_title})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LettersAPITest(TestCase):

    def test_get_3_letters(self):
        url = reverse('get_letters')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('letters', response.data)
        self.assertEqual(len(response.data['letters']), 3)

        for letter in response.data['letters']:
            self.assertIsInstance(letter, str)
            self.assertEqual(len(letter), 1)
'''
class EquationFunctionTest(TestCase):

    def setUp(self):
        self.user = customuser.objects.create_user(email='testuser', password='testpassword')
        

    def test_create_equation(self):
        request = self.client.get('/')
        request.user = self.user
        equation = create_3_equations(request)
        self.assertIn('num1', equation)
        self.assertIn('num2', equation)
        self.assertIn('op', equation)
        self.assertIn('result', equation)

'''