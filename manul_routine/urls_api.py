from rest_framework.routers import DefaultRouter
from django.conf.urls import  include
from django.urls import path
import boardapp.views as boardapp_view
import taskapp.views as taskapp_view


router = DefaultRouter()

router = DefaultRouter()
router.register(r'board', boardapp_view.BoardViewSet, basename='board')
router.register(r'column', boardapp_view.ColumnViewSet, basename='column')
router.register(r'task', taskapp_view.TaskViewSet, basename='task')
router.register(r'comment', taskapp_view.CommentViewSet, basename='comment')

urlpatterns =[path('api/', include(router.urls))]