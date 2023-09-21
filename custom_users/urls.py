from django.urls import path
from .views import register_user, user_login, user_logout,VerifyCode,change_password,get_user_profile,CreateKidView

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('verify/', VerifyCode.as_view(), name='verify_code'),
    path('profile/',get_user_profile, name='profile'),
    path('createKid/',CreateKidView.as_view(), name='createkid'),
]
