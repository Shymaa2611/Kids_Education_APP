from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category
from .serializers import categorySerializers


@api_view(['GET'])
def get_Categories(request):
    data = Category.objects.filter(
      category_title=request.data['category_title']
    )
    serializer=categorySerializers(data,many=True)
    return Response(serializer.data)
