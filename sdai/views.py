from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SDXLImageGenerationSerializer
from .tasks import send_generation_request_to_sdxl_task


class SDXLView(APIView):
    serializer_class = SDXLImageGenerationSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            task = send_generation_request_to_sdxl_task.delay(serializer.data)
            return Response({"task_id": task.id}, status=201)
        return Response(serializer.errors, status=400)
