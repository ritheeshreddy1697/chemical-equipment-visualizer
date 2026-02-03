from django.urls import path
from .views import UploadCSVAPIView, GeneratePDFAPIView

urlpatterns = [
    path("upload/", UploadCSVAPIView.as_view(), name="upload-csv"),
    path("report/", GeneratePDFAPIView.as_view(), name="generate-pdf"),
]