from taskapp.models import Task, Comment
from tools.serializers import ModelSerializerId
from rest_framework import serializers
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status


class CommentInlineSerializer(ModelSerializerId):
    class Meta:
        model = Comment
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

        
class TaskInlineSerializer(ModelSerializerId):
    comment_set = CommentInlineSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    comment_set = CommentInlineSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = "__all__"

