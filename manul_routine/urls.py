from django.contrib import admin
from django.urls import path,re_path,include
from django.conf.urls import  include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from boardapp.views import IndexView
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as authViews
# from rest_framework.authtoken import views
# admin.site.site_header = 'Manul routine'
# admin.site.site_title = 'Manul routine'


urlpatterns = [
    path('',IndexView.as_view()),
    path('accounts/login/', LoginView.as_view(template_name='login.html'),name="login"),
    path('exit/', authViews.LogoutView.as_view(next_page='/accounts/login/'), name='exit'),
    path('api-auth/', include('rest_framework.urls')),
    # path(r'api-token-auth/', views.obtain_auth_token),
    path(r'', include('manul_routine.urls_api')),
    path('admin/', admin.site.urls),
]+  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
