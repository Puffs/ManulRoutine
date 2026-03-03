from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django_filters import FilterSet, ModelMultipleChoiceFilter
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from boardapp.serializers import BoardSerializer, ColumnSerializer
from boardapp.models import Board, Column
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions, IsAuthenticatedOrReadOnly
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Prefetch
from taskapp.models import Task
from django.core.files.base import ContentFile
import base64
from userapp.models import CustomUser
# from django.contrib.auth.decorators import login_required


class IndexView(LoginRequiredMixin,TemplateView):
    template_name=  "index.html"
    login_url = "/accounts/login/"


class BoardSetFilter(FilterSet):

    def filter_queryset(self, request):
        user = self.request.user
        return Board.objects.filter(user_list=user)

    class Meta:
        model = Board
        fields= '__all__'
        exclude=['background_image']

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.filter()
    model = Board
    serializer_class = BoardSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filterset_class  = BoardSetFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def remove_user(self, request, pk):
        board_obj = Board.objects.get(id=pk)
        user_id = request.data.get("user_id")
        user_obj = CustomUser.objects.get(id=user_id)
        board_obj.user_list.remove(user_obj)

        return JsonResponse(pk, safe=False)
    
    @action(detail=True, methods=['post'])
    def add_user(self, request, pk):
        board_obj = Board.objects.get(id=pk)
        user_id = request.data.get("user_id")
        user_obj = CustomUser.objects.get(id=user_id)
        board_obj.user_list.add(user_obj)
        return JsonResponse(pk, safe=False)
    
    @action(detail=False, methods=['get'])
    def get_user_tasks(self, request):
        result_list = []
        board_dict = {}
        for task in Task.objects.filter(executor=request.user):
            executor_list = [{"id": executor.id, "username": executor.username} for executor in task.executor.all()]

            task_obj = {
                "id":task.id,
                "name":task.name,
                "executor":executor_list,
                "order":task.order,
                "column_id":task.column.id,
                "column_name":task.column.name,
            }
            if task.column.board.id not in board_dict:
                board_dict[task.column.board.id] = {
                    "id": task.column.board.id,
                    "name": task.column.board.name,
                    "task_set": [task_obj]
                }
            else:
                board_dict[task.column.board.id]["task_set"].append(task_obj)

        result_list = sorted(board_dict.values(), key=lambda x: x["id"])

        return JsonResponse(result_list, safe=False)

    @action(detail=True, methods=['post'])
    def save_board_image(self, request, pk):
        img = request.data.get('background_image')
        board_obj = Board.objects.get(id=pk)

        format, imgstr = img.split(';base64,')
        ext = format.split('/')[-1]
        
        image_data = base64.b64decode(imgstr)
        file_name = f'background_{pk}.{ext}'
        
        board_obj.background_image.save(file_name, ContentFile(image_data), save=True)
        
        return JsonResponse(pk, safe=False)
    
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
        Column.objects.create(name="Backlog", order=0, board=instance)
        Column.objects.create(name="ToDo", order=1, board=instance)
        Column.objects.create(name="In progress", order=2, board=instance)
        Column.objects.create(name="Done", order=3, board=instance)
    