from django.urls import path

from .views import SDXLView

urlpatterns = [
    path("sdxl/", SDXLView.as_view()),
]
