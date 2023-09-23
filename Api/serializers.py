from rest_framework import serializers
from .models import Category


class categorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('category_title','image')
