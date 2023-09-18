from rest_framework import serializers
from .models import customuser
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

    class Meta:
        model = customuser
        fields = ['first_name', 'last_name', 'email', 'password', 'privacy_security']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        privacy_security = validated_data.get('privacy_security', False)
        email = validated_data.get('email')
        if privacy_security:
            user = customuser(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                privacy_security=validated_data['privacy_security'],
                email=email
            )
            user.set_password(validated_data['password'])
            user.save()
            verification_code = generate_verification_code()
            send_verification_email(email, verification_code)
            expiration_time = timezone.now() + timezone.timedelta(minutes=30)
            Verification.objects.create(user=user, code=verification_code, expiration_time=expiration_time)
            return user
        else:
            raise serializers.ValidationError("Privacy security must be true to create a user.")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)