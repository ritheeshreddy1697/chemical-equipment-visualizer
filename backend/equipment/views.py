from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator




from rest_framework.permissions import AllowAny

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from django.http import FileResponse
from .pdf_utils import generate_pdf



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import analyze_csv
from .models import Dataset

@method_decorator(csrf_exempt, name='dispatch')
class UploadCSVAPIView(APIView):
    authentication_classes = []   # 🔑 disable auth
    permission_classes = [AllowAny]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {"error": "CSV file not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['file']

        try:
            summary = analyze_csv(file)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        Dataset.objects.create(
            filename=file.name,
            total_equipment=summary["total_count"],
            avg_flowrate=summary["avg_flowrate"],
            avg_pressure=summary["avg_pressure"],
            avg_temperature=summary["avg_temperature"],
        )

        if Dataset.objects.count() > 5:
            Dataset.objects.order_by('uploaded_at').first().delete()

        return Response(summary, status=status.HTTP_200_OK)
class UploadHistoryAPIView(APIView):

    def get(self, request):
        datasets = Dataset.objects.order_by('-uploaded_at')[:5]

        history = []
        for d in datasets:
            history.append({
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "total_equipment": d.total_equipment,
                "avg_flowrate": d.avg_flowrate,
                "avg_pressure": d.avg_pressure,
                "avg_temperature": d.avg_temperature,
            })

        return Response(history)
@method_decorator(csrf_exempt, name='dispatch')
class GeneratePDFAPIView(APIView):
    authentication_classes = []   # 🔑 disable auth
    permission_classes = [AllowAny]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "CSV file not provided"}, status=400)

        file = request.FILES['file']
        summary = analyze_csv(file)

        pdf_path = generate_pdf(summary)

        return FileResponse(
            open(pdf_path, "rb"),
            as_attachment=True,
            filename="equipment_report.pdf"
        )
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "Backend is running",
        "project": "Chemical Equipment Parameter Visualizer",
        "backend": "Django + Django REST Framework",
    })
