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
from django import forms
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import login

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



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Пароли не совпадают.")
        

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect('/')
            except ValidationError as e:
                form.add_error('username', e)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})