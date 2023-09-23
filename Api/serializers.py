from rest_framework import serializers
from .models import Category,Challenge,Content


class categorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('category_title','image')


class contentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('content','kid_age')

class challengeSerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('title','image','category')
