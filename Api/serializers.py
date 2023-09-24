from rest_framework import serializers
from .models import Category,Challenge,Content


class categorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('category_title','image')

class contentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields=('content',)

class challengeSerializers(serializers.ModelSerializer):
    category_title = serializers.ReadOnlyField(source='category.category_title')
    
    def to_representation(self, instance):
        authenticated_user = self.context.get('request').user
        
        user_kid = authenticated_user.kid
        user_age = user_kid.age
        content = instance.content.filter(kid_age=user_age)
        
        content_serializer = contentSerializers(content, many=True)
        
        if not content_serializer.data:
            return None 
        
        return {
            'title': instance.title,
            'image': instance.image.url if instance.image else None,
            'category_title': instance.category.category_title,
            'content': content_serializer.data
        }

    class Meta:
        model = Challenge
        fields = ('title', 'image', 'category', 'category_title', 'content')
