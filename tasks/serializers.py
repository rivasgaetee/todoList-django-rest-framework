from rest_framework import serializers
from .models import Task, TaskStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'


class TaskReadSerializer(serializers.ModelSerializer):
    status = TaskStatusSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class TaskWriteSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=TaskStatus.objects.all())

    class Meta:
        model = Task
        fields = '__all__'
