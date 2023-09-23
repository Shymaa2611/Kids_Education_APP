from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category,Content,Challenge
from rest_framework.views import APIView
from .serializers import categorySerializers,contentSerializers,challengeSerializers
import numpy as np
import pandas as pd

@api_view(['GET'])
def get_Categories(request):
    data = Category.objects.all()
    serializer = categorySerializers(data, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def search_Category(request):
    data = Challenge.objects.filter(
      category=request.data['category']
    )
    serializer=categorySerializers(data,many=True)
    return Response(serializer.data)

def create_Equation():
        equations=0
        num1=np.random.randint(1,100)
        num2=np.random.randint(1,100)
        index=np.random.randint(1,4)
        if index==1:
            result=num1+num2
            equations={'num1':num1,'num2':num2,'op':'+','result':result}
        elif index==2:
            if num1>num2:
                result=num1-num2
                equations={'num1':num1,'num2':num2,'op':'-','result':result}
            else:
                result=num2-num1
                equations={'num1':num2,'num2':num1,'op':'-','result':result}
        elif index==3:
            result=num1/num2
            equations={'num1':num1,'num2':num2,'op':'/','result':int(result)}
        elif index==4:
            result=num1*num2
            equations={'num1':num1,'num2':num2,'op':'*','result':result}
            
        return equations

@api_view(['GET'])
def create_3_equations(request):
      equation=[]
      for i in range(3):
           eq=create_Equation()
           equation.append(eq)
      request.session['result1']=equation[0]['result']
      request.session['result2']=equation[1]['result']
      request.session['result3']=equation[2]['result']       
      response={
                  "results":equation
              }
      return Response(response,status=status.HTTP_200_OK)

@api_view(['POST'])
def check_results(request):
     result1 = request.data.get('result1')
     result2 = request.data.get('result2')
     result3 = request.data.get('result3')
     answer1=request.session.get('result1',None)
     answer2=request.session.get('result2',None)
     answer3=request.session.get('result3',None)
     print(answer1)
     print(result2)
     print(result3)
     if result1==answer1 and result2==answer2 and result3==answer3:
          return Response({'message':'Great Job'},status=status.HTTP_200_OK)
     else:
          return Response({'message':'Try Again'},status=status.HTTP_400_BAD_REQUEST)


class ContentForUserAgeView(APIView):
    def get(self, request, format=None):
        user_kid = request.user.kid
        if user_kid:
            user_age = user_kid.age
            content_for_user_age = Content.objects.filter(kid_age=user_age)
            serializer = contentSerializers(content_for_user_age, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User does not have a related Kid object"}, status=status.HTTP_404_NOT_FOUND)


