from django.urls import path
from .views import (
    register_user,user_login, user_logout,VerifyCode,change_password,
    get_user_profile,CreateKidView,kid_access_code_login,send_forgot_password_verification_code,
    UpdateKidAPIView,VerifyCode_rest_password)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('verify/', VerifyCode.as_view(), name='verify_code'),
    path('verify_rest_password/', VerifyCode_rest_password.as_view(), name='verify_rest_password'),
    path('profile/',get_user_profile, name='profile'),
    path('createKid/',CreateKidView.as_view(), name='createkid'),
    path('kid_login/',kid_access_code_login, name='kid_access'),
    path('send_forgot_password_code/',send_forgot_password_verification_code, name='send_forgot_password_code'),
    path('update_kid/', UpdateKidAPIView.as_view(), name='update_kid'),
]
