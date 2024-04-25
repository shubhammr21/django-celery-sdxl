from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import get_tasks


class TaskListView(APIView):
    """
    View to list all tasks in Celery
    """

    def get(self, request):
        task_data = get_tasks()
        return Response(task_data)


class TaskDetailView(APIView):
    """
    View to get details of a specific task by task_id
    """

    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        data = {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result,
        }
        return Response(data)
