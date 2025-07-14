from django.contrib import admin
from django.urls import path,re_path,include
from django.conf.urls import  include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from boardapp.views import IndexView
# admin.site.site_header = 'Manul routine'
# admin.site.site_title = 'Manul routine'


urlpatterns = [
    path('',IndexView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path(r'', include('manul_routine.urls_api')),
    path('admin/', admin.site.urls),
]+  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# ]+  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
