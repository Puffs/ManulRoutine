from userapp.models import CustomUser
from tools.serializers import ModelSerializerId
from rest_framework import serializers
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status


class CustomUserInlineSerializer(ModelSerializerId):
    class Meta:
        model = CustomUser
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"