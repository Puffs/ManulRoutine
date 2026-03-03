from userapp.models import CustomUser
from tools.serializers import ModelSerializerId
from rest_framework import serializers

    
class CustomUserInlineSerializer(ModelSerializerId):
    username = serializers.CharField(max_length=50)
    avatar_url = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        exclude = ['password']

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None
    
class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        exclude = ['password']

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None
