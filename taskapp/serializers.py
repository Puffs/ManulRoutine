from taskapp.models import Task
from tools.serializers import ModelSerializerId
from rest_framework import serializers
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status

class TaskInlineSerializer(ModelSerializerId):
    class Meta:
        model = Task
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"