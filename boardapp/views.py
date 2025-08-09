from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django_filters import FilterSet
from django_filters import filters
from rest_framework import viewsets,permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
import os
from django.conf import settings
from boardapp.serializers import BoardSerializer, ColumnSerializer
from boardapp.models import Board, Column
from django.http import JsonResponse
from rest_framework.permissions import BasePermission,IsAuthenticated,DjangoModelPermissions
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Prefetch
from taskapp.models import Task
# from django.contrib.auth.decorators import login_required


class IndexView(LoginRequiredMixin,TemplateView):
    template_name=  "index.html"
    login_url = "/accounts/login/"


class BoardSetFilter(FilterSet):
    class Meta:
        model = Board
        fields= '__all__'

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.filter()
    model = Board
    serializer_class = BoardSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filterset_class  = BoardSetFilter
    permission_classes = [IsAuthenticated,DjangoModelPermissions]


class ColumnSetFilter(FilterSet):
    class Meta:
        model = Column
        fields= '__all__'

class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.filter().order_by('order').prefetch_related(Prefetch('task_set', queryset=Task.objects.order_by('order')))
    model = Column
    serializer_class = ColumnSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filterset_class  = ColumnSetFilter
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    
    @action(detail=False, methods=['post'])
    def set_column_order(self, request):
        order_list = request.data
        for col in order_list:
            col_obj = Column.objects.get(id=col["id"])
            col_obj.order = col["order"]
            col_obj.save()
        
        return JsonResponse({}, safe=False)
    
@receiver(post_save, sender=Board)
def my_model_post_save(sender, instance, created, **kwargs):
    if created:
        Column.objects.create(name="ToDo", order=0, board=instance)
        Column.objects.create(name="In progress", order=1, board=instance)
        Column.objects.create(name="Done", order=2, board=instance)
    