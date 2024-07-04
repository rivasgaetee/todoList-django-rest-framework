from rest_framework import viewsets
from .models import Task
from .serializers import TaskReadSerializer, TaskWriteSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return TaskWriteSerializer
        return TaskReadSerializer
