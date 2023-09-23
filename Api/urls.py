from django.urls import path

from . import views

urlpatterns = [
   path('get_categories/', views.get_Categories, name='get_categories'),
   path('get_category/', views.search_Category, name='get_category'),
   path('create_equations/', views.create_3_equations, name='create_equation'),
   path('check_results/', views.check_results, name='check_results'),
]
