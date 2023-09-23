from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer,ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import customuser,Verification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Profile,Kid
from .serializers import ProfileSerializer,kidSerializer,generate_verification_code,send_verification_email
from rest_framework.generics import RetrieveUpdateAPIView

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = None
        if '@' in email:
            try:
                user = customuser.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response({'message':'invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if not user:
            user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def kid_access_code_login(request):
    access_code = request.data.get('access_code')
    
    try:
        kid = Kid.objects.get(access_code=access_code)
        user = customuser.objects.get(kid=kid)
        print(user.email)
    except (Kid.DoesNotExist, customuser.DoesNotExist):
        return Response({'error': 'Invalid access code'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user:
        user = authenticate(email=user.email, password=user.password)

    if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        user = request.user
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if old_password==user.password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user) 
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_forgot_password_verification_code(request):
    if request.method=='POST':
         email = request.data.get('email')
         code=generate_verification_code()
         request.session['verification_email'] = email
         send_verification_email(email,code)
         return Response({'message':'successfully '}, status=status.HTTP_200_OK)
    return Response({'message':'something is wrong'}, status=status.HTTP_400_BAD_REQUEST)

class KidUpdate(RetrieveUpdateAPIView):
    serializer_class = kidSerializer
    permission_classes = [IsAuthenticated,]
    def get_object(self):
        return self.request.user 
    def perform_update(self, serializer):
        serializer.save()



class VerifyCode(APIView):
    def post(self, request):
        code = request.data.get('code')
        email = request.session.get('verification_email',None) 
        user = customuser.objects.get(email=email)
        try:
            verification = Verification.objects.get(user=user, code=code)

            if verification.is_expired():
                return Response({'message': 'Code has expired'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = verification.user
                user.is_verified = True
                user.save()
                verification.delete()
                
                return Response({'message': 'Code verified successfully'}, status=status.HTTP_200_OK)
        except Verification.DoesNotExist:
            return Response({'message': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)

class CreateKidView(APIView):
    def post(self, request, format=None):
        access_code = request.data.get('access_code')
        if Kid.objects.filter(access_code=access_code).exists():
            return Response({'detail': 'Access code already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = customuser.objects.last()

        serializer = kidSerializer(data=request.data)

        if serializer.is_valid():
            kid = serializer.save()
            user.kid = kid 
            user.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response({'message': 'Profile not found'}, status=404)