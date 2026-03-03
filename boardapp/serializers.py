from boardapp.models import Board, Column
from tools.serializers import ModelSerializerId
from rest_framework import serializers
from taskapp.serializers import TaskInlineSerializer
from userapp.serializers import CustomUserSerializer
from rest_framework.exceptions import ValidationError

class BoardInlineSerializer(ModelSerializerId):
    
    class Meta:
        model = Board
        fields = "__all__"

class BoardSerializer(serializers.ModelSerializer):
    background_image_url = serializers.SerializerMethodField()

    def validate_name(self, value):
        if len(value) < 4:
            raise ValidationError("Название доски должно содержать 4 или более символов")

    class Meta:
        model = Board
        fields = "__all__"

    # def update(self,instance,validated_data):
    #     executor_set = validated_data.pop('executor', None)
        
    #     if executor_set is not None:
    #         instance.executor.set(executor_set)
    #     return super().update(instance,validated_data)

    def get_background_image_url(self, obj):
        return obj.background_image.url if obj.background_image else None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_list'] = CustomUserSerializer(instance.user_list.all(), many=True).data
        return representation
    
    def to_internal_value(self, data):
        if 'user_list' in data:
            user_list_data = data['user_list']
        
            if all(isinstance(item, dict) for item in user_list_data):
                executor_ids = [item['id'] for item in user_list_data]
                data['user_list'] = executor_ids
            elif all(isinstance(item, int) for item in user_list_data):
                pass
            else:
                raise serializers.ValidationError("executor must be a list of IDs or objects.")
        
        return super().to_internal_value(data)
    
class ColumnInlineSerializer(ModelSerializerId):

    class Meta:
        model = Column
        fields = "__all__"

class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskInlineSerializer(many=True, source="task_set", read_only=True)

    class Meta:
        model = Column
        fields = "__all__"