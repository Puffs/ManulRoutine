from boardapp.models import Board, Column
from tools.serializers import ModelSerializerId
from rest_framework import serializers
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status
from taskapp.serializers import TaskInlineSerializer

class BoardInlineSerializer(ModelSerializerId):
    class Meta:
        model = Board
        fields = "__all__"

class BoardSerializer(serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = "__all__"

    def get_background_image_url(self, obj):
        return obj.background_image.url if obj.background_image else None
    
class ColumnInlineSerializer(ModelSerializerId):
    class Meta:
        model = Column
        fields = "__all__"

class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskInlineSerializer(many=True, source="task_set", read_only=True)
    class Meta:
        model = Column
        fields = "__all__"