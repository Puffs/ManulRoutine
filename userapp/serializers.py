from userapp.models import CustomUser
from tools.serializers import ModelSerializerId
from rest_framework import serializers


# class CustomUserSelectiveSerializer(serializers.ModelSerializer):
#     avatar_url = serializers.SerializerMethodField()
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'avatar_url']
#     def get_avatar_url(self, obj):
#         return obj.avatar.url if obj.avatar else None
    
class CustomUserInlineSerializer(ModelSerializerId):
    
    class Meta:
        model = CustomUser
        exclude = ['password']

class CustomUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        exclude = ['password']
    
    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None