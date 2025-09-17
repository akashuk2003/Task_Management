from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskCompletionSerializer, TaskReportSerializer
from .permissions import IsSuperAdmin, IsAdmin, IsUser

#TASK API VIEWS
class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

#TASK COMPLETION VIEW FOR USERS
class TaskCompleteAPIView(generics.UpdateAPIView):
    serializer_class = TaskCompletionSerializer
    permission_classes = [IsAuthenticated, IsUser]
    queryset = Task.objects.all()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.completion_report = serializer.validated_data['completion_report']
        instance.worked_hours = serializer.validated_data['worked_hours']
        instance.status = 'Completed'
        instance.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

#TASK REPORT VIEW FOR ADMIN AND SUPERADMIN
class TaskReportAPIView(generics.RetrieveAPIView):
    serializer_class = TaskReportSerializer
    permission_classes = [IsAuthenticated, (IsAdmin | IsSuperAdmin)]

    def get_queryset(self):
        return Task.objects.filter(status='Completed')