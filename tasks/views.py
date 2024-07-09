from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Task, CustomUser
from .serializers import TaskReadSerializer, TaskWriteSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskReadSerializer
        return TaskWriteSerializer

    def create(self, request, *args, **kwargs):
        user_payload = request.user
        user, created = CustomUser.objects.get_or_create(user_id=user_payload['sub'], defaults={
            'email': user_payload.get('email', ''),
            'name': user_payload.get('name', ''),
        })
        print(f"User: {user}, Created: {created}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        read_serializer = TaskReadSerializer(serializer.instance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        read_serializer = TaskReadSerializer(serializer.instance)
        return Response(read_serializer.data)
