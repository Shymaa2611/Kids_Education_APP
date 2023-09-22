from rest_framework import serializers
from .models import customuser,Kid,Profile
from django.conf import settings
from django.core.mail import send_mail
from .models import Verification
from django.utils import timezone
import random

def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_verification_email(email, code):
    subject = 'Verification code for your account'
    message = f'Your verification code is: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, max_length=20)

    class Meta:
        model = customuser
        fields = ['first_name', 'last_name', 'email', 'password', 'privacy_security', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})

        return data

    def create(self, validated_data):
        privacy_security = validated_data.get('privacy_security', False)
        email = validated_data.get('email')
        password = validated_data.get('password')
        if privacy_security:
            user = customuser(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                privacy_security=validated_data['privacy_security'],
                email=email
            )
            user.set_password(password)
            user.save()
            verification_code = generate_verification_code()
            send_verification_email(email, verification_code)
            expiration_time = timezone.now() + timezone.timedelta(minutes=30)
            Verification.objects.create(user=user, code=verification_code, expiration_time=expiration_time)
            request = self.context.get('request')
            if request:
                request.session['verification_email'] = email

            return user
        else:
            raise serializers.ValidationError("Privacy security must be true to create a user.")

class kidSerializer(serializers.ModelSerializer):
    class Meta:
        model=Kid
        fields=['name','age','gender','password','access_code']



class ProfileSerializer(serializers.ModelSerializer):
    kid = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()  

    class Meta:
        model = Profile
        fields = ['user', 'email', 'kid']

    def get_kid(self, obj):
        user = obj.user
        if user.kid:
            kid_data = {
                'name': user.kid.name,
                'password': user.password,
                'access_code': user.kid.access_code
            }
            return kid_data
        else:
            return None

    def get_email(self, obj): 
        return obj.user.email



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)


""" class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification_code = generate_verification_code()
    send_verification_email(email, verification_code)
 """