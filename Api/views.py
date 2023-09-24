from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category,Challenge
from .serializers import categorySerializers,challengeSerializers
import numpy as np
import string
import random

@api_view(['GET'])
def get_Categories(request):
    data = Category.objects.all()
    serializer = categorySerializers(data, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_Challenge(request):
    category_title = request.data.get('category') 
    data = Challenge.objects.filter(category__category_title=category_title)
    serializer = challengeSerializers(data, many=True,context={'request': request})
    return Response(serializer.data)


def create_Equation(request):
        user=request.user
        end=0
        if user.kid.age>=3 and user.kid.age<5:
             end=20
        elif user.kid.age>=5 and user.kid.age<=7:
             end=60
        else:
             end=100
        equations=0
        num1=np.random.randint(1,end)
        num2=np.random.randint(1,end)
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
            if num1>num2:
              result=num1/num2
              equations={'num1':num1,'num2':num2,'op':'/','result':int(result)}
            else:
                 result=num2/num1
                 equations={'num1':num2,'num2':num1,'op':'/','result':int(result)}

        elif index==4:
            result=num1*num2
            equations={'num1':num1,'num2':num2,'op':'*','result':result}
            
        return equations

@api_view(['GET'])
def create_3_equations(request):
      equation=[]
      for i in range(3):
           eq=create_Equation(request)
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
     result1 =str(request.data.get('result1'))
     result2 =str(request.data.get('result2'))
     result3 =str(request.data.get('result3'))
     answer1=str(request.session.get('result1',None))
     answer2=str(request.session.get('result2',None))
     answer3=str(request.session.get('result3',None))
     print(answer1)
     print(answer2)
     print(answer3)
     if result1==answer1 and result2==answer2 and result3==answer3:
          return Response({'message':'Great Job'},status=status.HTTP_200_OK)
     else:
          return Response({'message':'Try Again'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_3_letters(request):
    random_chars = random.sample(string.ascii_letters, 3)
    request.session['letter1']=random_chars[0]
    request.session['letter2']=random_chars[1]
    request.session['letter3']=random_chars[2]       
    response={
         "letters":random_chars
    }
    return Response(response,status=status.HTTP_200_OK)


@api_view(['POST'])
def check_answer(request):
     letter1 =request.data.get('letter1')
     letter2 =request.data.get('letter2')
     letter3 =request.data.get('letter3')
     answer1=request.session.get('letter1',None)
     answer2=request.session.get('letter2',None)
     answer3=request.session.get('letter3',None)
     print(answer1)
     print(answer2)
     print(answer3)
     if letter1==answer1 and letter2==answer2 and letter3==answer3:
          return Response({'message':'Great Job'},status=status.HTTP_200_OK)
     else:
          return Response({'message':'Try Again'},status=status.HTTP_400_BAD_REQUEST)


games=['Letters','Math','Alphabeta','Color & shape']


