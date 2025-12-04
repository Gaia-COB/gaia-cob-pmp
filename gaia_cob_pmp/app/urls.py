from django.urls import path

from app.views import download_dataset_view

urlpatterns = [path("download/<dataset_pk>", download_dataset_view, name="download-dataset")]
