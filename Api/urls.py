from django.urls import path

from . import views

urlpatterns = [
   path('get_categories/', views.get_Categories, name='get_categories'),
   path('get_category/', views.search_Category, name='get_category'),
]
