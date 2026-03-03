from django.shortcuts import render
from django_filters import FilterSet
from django_filters import filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from userapp.serializers import CustomUserSerializer
from userapp.models import CustomUser
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from django import forms
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import login
from django.core.files.base import ContentFile
import base64


class CustomUserSetFilter(FilterSet):
    
    class Meta:
        model = CustomUser
        fields= '__all__'
        exclude = ['avatar']

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter()
    model = CustomUser
    serializer_class = CustomUserSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filterset_class  = CustomUserSetFilter
    permission_classes = [IsAuthenticated,DjangoModelPermissions]

    @action(detail=False,methods=['get'])
    def who_im(self,request):
        user_dict = CustomUserSerializer(request.user)
        return Response(user_dict.data)

    
    @action(detail=True, methods=['post'])
    def save_avatar_image(self, request, pk):
        img = request.data.get('avatar_image')
        user_obj = CustomUser.objects.get(id=pk)

        format, imgstr = img.split(';base64,')
        ext = format.split('/')[-1]
        
       
        image_data = base64.b64decode(imgstr)
        file_name = f'avatar_{pk}.{ext}'
        
        user_obj.avatar.save(file_name, ContentFile(image_data), save=True)
        
        return JsonResponse(pk, safe=False)


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