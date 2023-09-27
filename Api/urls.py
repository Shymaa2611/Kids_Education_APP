from django.urls import path

from . import views

urlpatterns = [
   path('get_categories/', views.get_Categories, name='get_categories'),
   path('get_challenge/', views.get_Challenge, name='get_Challenge'),
   #path('get_equations/', views.create_3_equations, name='create_equation'),
   #path('check_results/', views.check_results, name='check_results'),
   #path('get_letters/', views.get_3_letters, name='get_letters'),
   #path('check_answer/', views.check_answer, name='check_answer'),
   #path('get_Numbers/', views.create_3_numbers, name='get_Numbers'),
   #path('check_numbers/', views.check_Numbers, name='check_numbers'),
   path('Game/', views.Games, name='Game'),
   path('Check/', views.check, name='Check'),

]
