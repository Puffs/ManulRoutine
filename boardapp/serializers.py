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
    class Meta:
        model = Board
        fields = "__all__"

class ColumnInlineSerializer(ModelSerializerId):
    class Meta:
        model = Column
        fields = "__all__"

class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskInlineSerializer(many=True, source="task_set", required=False)
    class Meta:
        model = Column
        fields = "__all__"