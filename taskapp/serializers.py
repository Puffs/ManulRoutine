from taskapp.models import Task, Comment
from tools.serializers import ModelSerializerId
from rest_framework import serializers
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status
from userapp.models import CustomUser
from userapp.serializers import CustomUserSerializer

    
class CommentInlineSerializer(ModelSerializerId):
    date= serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True,
    )
    author = CustomUserSerializer(read_only=True)
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
    executor = CustomUserSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    comment_set = CommentInlineSerializer(many=True, read_only=True)
    executor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),many=True)
    class Meta:
        model = Task
        fields = "__all__"

    def update(self,instance,validated_data):
        executor_set = validated_data.pop('executor', None)
        
        if executor_set is not None:
            instance.executor.set(executor_set)
        return super().update(instance,validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['executor'] = CustomUserSerializer(instance.executor.all(), many=True).data
        return representation
