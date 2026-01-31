from django.urls import path
from .views import UploadCSVAPIView, UploadHistoryAPIView, GeneratePDFAPIView

urlpatterns = [
    path("upload/", UploadCSVAPIView.as_view(), name="upload-csv"),
    path("history/", UploadHistoryAPIView.as_view(), name="upload-history"),
    path("report/", GeneratePDFAPIView.as_view(), name="generate-pdf"),
]
