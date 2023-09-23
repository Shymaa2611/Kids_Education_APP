from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category
from .serializers import categorySerializers
import numpy as np
import pandas as pd

@api_view(['GET'])
def get_Categories(request):
    data = Category.objects.all()
    serializer = categorySerializers(data, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def search_Category(request):
    data = Category.objects.filter(
      category_title=request.data['category_title']
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


      response={
                  "results":equation
              }
      return Response(response,status=status.HTTP_200_OK)


