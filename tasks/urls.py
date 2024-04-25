from django.urls import path

from .views import TaskDetailView, TaskListView

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("<str:task_id>/", TaskDetailView.as_view(), name="task-detail"),
]
