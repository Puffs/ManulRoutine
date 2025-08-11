from taskapp.models import Task, Comment
from tools.serializers import ModelSerializerId
from rest_framework import serializers
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status
from userapp.models import CustomUser
from userapp.serializers import CustomUserSelectiveSerializer

    
class CommentInlineSerializer(ModelSerializerId):
    date= serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True,
    )
    author = CustomUserSelectiveSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    date= serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True,
    )
    class Meta:
        model = Comment
        fields = "__all__"

        
class TaskInlineSerializer(ModelSerializerId):
    comment_set = CommentInlineSerializer(many=True, read_only=True)
    executor = CustomUserSelectiveSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    comment_set = CommentInlineSerializer(many=True, read_only=True)
    executor = CustomUserSelectiveSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = "__all__"

