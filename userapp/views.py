from django.shortcuts import render
from django_filters import FilterSet
from django_filters import filters
from rest_framework import viewsets,permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
import os
from django.conf import settings
from userapp.serializers import CustomUserSerializer
from userapp.models import CustomUser
from django.http import JsonResponse
from rest_framework.permissions import BasePermission,IsAuthenticated,DjangoModelPermissions


    
class CustomUserSetFilter(FilterSet):
    class Meta:
        model = CustomUser
        fields= '__all__'

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter()
    model = CustomUser
    serializer_class = CustomUserSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filterset_class  = CustomUserSetFilter
    permission_classes = [IsAuthenticated,DjangoModelPermissions]