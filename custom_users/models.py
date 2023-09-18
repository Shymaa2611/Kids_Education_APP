from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from django.utils import timezone

class customuser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email = models.EmailField(unique=True) 
    privacy_security = models.BooleanField(default=False)  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    


class Verification(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()

    def is_expired(self):
        return self.expiration_time < timezone.now()
Gender=[
    ("male","male"),
    ("female","female")
]
class Kid(models.Model):
    parent=models.ForeignKey(customuser,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    age=models.IntegerField(default=5)
    gender=models.CharField(max_length=6,choices=Gender)
    access_code=models.IntegerField(default=0)
    def __str__(self):
        return self.name
    

class Profile(models.Model):
    kid=models.ForeignKey(Kid,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile/images/')


