from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
Gender=[
    ("male","male"),
    ("female","female")
]
class Kid(models.Model):
    name=models.CharField(max_length=20)
    image=image=models.ImageField(upload_to='profile/images/',blank=True,null=True)
    age=models.IntegerField(default=5)
    gender=models.CharField(max_length=6,choices=Gender)
    password=models.CharField(max_length=20)
    access_code=models.IntegerField(default=0)
    def __str__(self):
        return self.name
    


class customuser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email = models.EmailField(unique=True) 
    privacy_security = models.BooleanField(default=False)  
    kid=models.ForeignKey(Kid,on_delete=models.CASCADE,blank=True,null=True)
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


class Profile(models.Model):
    user=models.OneToOneField(customuser,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.email} Profile"

@receiver(post_save, sender=customuser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


    




