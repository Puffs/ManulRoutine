from django.shortcuts import render
from django_filters import FilterSet
from django_filters import filters
from rest_framework import viewsets,permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
import os
from django.conf import settings
from taskapp.serializers import TaskSerializer, CommentSerializer
from taskapp.models import Task, Comment
from django.http import JsonResponse
from rest_framework.permissions import BasePermission,IsAuthenticated,DjangoModelPermissions



class TaskSetFilter(FilterSet):
    class Meta:
        model = Task
        fields= '__all__'

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter().order_by("order")
    model = Task
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filterset_class  = TaskSetFilter
    permission_classes = [IsAuthenticated,DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def set_task_order(self, request):
        task_list = request.data
        for task in task_list:
            task_obj = Task.objects.get(id=task["id"])
            task_obj.order = task["order"]
            task_obj.save()
        
        return JsonResponse({}, safe=False)
    
class CommentSetFilter(FilterSet):
    class Meta:
        model = Comment
        fields= '__all__'

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter().order_by("date")
    model = Comment
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filterset_class  = CommentSetFilter
    permission_classes = [IsAuthenticated,DjangoModelPermissions]