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

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task

    def update(self, instance, validated_data):
        new_status = validated_data.get('status')

        if new_status and new_status.id == 3:
            instance.completed = True

        instance.status = new_status or instance.status
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
