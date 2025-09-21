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
    img_file_url = serializers.SerializerMethodField()
    data_url = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = "__all__"

    def get_img_file_url(self, obj):
        return obj.img_file.url if obj.img_file else None
    def get_data_url(self, obj):
        return obj.data.url if obj.data else None
    
class CommentSerializer(serializers.ModelSerializer):
    date= serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True,
    )
    data_url = serializers.SerializerMethodField()
    img_file_url = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = "__all__"

    def get_img_file_url(self, obj):
        return obj.img_file.url if obj.img_file else None
    def get_data_url(self, obj):
        return obj.data.url if obj.data else None
    
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
    
    def to_internal_value(self, data):
        if 'executor' in data:
            executor_data = data['executor']
        
            if all(isinstance(item, dict) for item in executor_data):
                executor_ids = [item['id'] for item in executor_data]
                data['executor'] = executor_ids
            elif all(isinstance(item, int) for item in executor_data):
                pass
            else:
                raise serializers.ValidationError("executor must be a list of IDs or objects.")
        
        return super().to_internal_value(data)
    