from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.api.models import Task
from apps.api.serializers import TaskSerializer, TaskDetailSerializer, TaskStatusUpdateSerializer


class TaskView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()


class TaskStatusUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskStatusUpdateSerializer
    queryset = Task.objects.all()
