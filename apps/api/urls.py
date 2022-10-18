from django.urls import path

from apps.api import views

urlpatterns = [
    path('todo/', views.TaskView.as_view()),
    path('todo/<int:pk>/', views.TaskDetailView.as_view()),
    path('todo/<int:pk>/execute/', views.TaskStatusUpdateView.as_view())
]