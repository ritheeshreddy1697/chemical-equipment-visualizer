import os
import tempfile
from datetime import datetime


import matplotlib
matplotlib.use("Agg")   # 🔑 REQUIRED for servers
import matplotlib.pyplot as plt
import pandas as pd

from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch


# =========================================================
# CSV ANALYSIS LOGIC
# =========================================================
def analyze_csv(file):
    df = pd.read_csv(file)

    # Normalize column names (basic safety)
    df.columns = [c.strip() for c in df.columns]

    total_count = len(df)

    avg_flowrate = df["Flowrate"].mean()
    avg_pressure = df["Pressure"].mean()
    avg_temperature = df["Temperature"].mean()

    type_distribution = df["Type"].value_counts().to_dict()

    table_data = df.to_dict(orient="records")

    return {
        "total_count": total_count,
        "avg_flowrate": avg_flowrate,
        "avg_pressure": avg_pressure,
        "avg_temperature": avg_temperature,
        "type_distribution": type_distribution,
        "table_data": table_data,
    }


# =========================================================
# BAR CHART GENERATOR (for PDF)
# =========================================================
def generate_bar_chart(type_distribution):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

    labels = list(type_distribution.keys())
    values = list(type_distribution.values())

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color="#f09819")
    plt.title("Equipment Type Distribution")
    plt.xlabel("Equipment Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(tmp_file.name)
    plt.close()

    return tmp_file.name


# =========================================================
# PDF GENERATION LOGIC
# =========================================================
def generate_pdf_report(summary, table_data):
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(pdf_file.name, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # ---------- TITLE ----------
    elements.append(
        Paragraph("<b>Chemical Equipment Analysis Report</b>", styles["Title"])
    )
    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 16))

    # ---------- SUMMARY TABLE ----------
    summary_table_data = [
        ["Metric", "Value"],
        ["Total Equipment", summary["total_count"]],
        ["Average Flowrate", f"{summary['avg_flowrate']:.2f}"],
        ["Average Pressure", f"{summary['avg_pressure']:.2f}"],
        ["Average Temperature", f"{summary['avg_temperature']:.2f}"],
    ]

    summary_table = Table(summary_table_data, colWidths=[3 * inch, 3 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.orange),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ]
        )
    )

    elements.append(Paragraph("<b>Summary Statistics</b>", styles["Heading2"]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # ---------- BAR CHART ----------
    chart_path = generate_bar_chart(summary["type_distribution"])
    elements.append(
        Paragraph("<b>Equipment Type Distribution</b>", styles["Heading2"])
    )
    elements.append(Spacer(1, 10))
    elements.append(Image(chart_path, width=5 * inch, height=3 * inch))
    elements.append(Spacer(1, 20))

    # ---------- DATA TABLE ----------
    elements.append(
        Paragraph("<b>Equipment Data (Preview)</b>", styles["Heading2"])
    )

    table_header = [
        "Equipment Name",
        "Type",
        "Flowrate",
        "Pressure",
        "Temperature",
    ]
    table_rows = [table_header]

    for row in table_data[:25]:
        table_rows.append(
            [
                row["Equipment Name"],
                row["Type"],
                row["Flowrate"],
                row["Pressure"],
                row["Temperature"],
            ]
        )

    data_table = Table(table_rows, repeatRows=1)
    data_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (2, 1), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ]
        )
    )

    elements.append(data_table)

    # ---------- BUILD PDF ----------
    doc.build(elements)
    os.remove(chart_path)

    return pdf_file.name


# =========================================================
# API VIEWS
# =========================================================
class UploadCSVAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if "file" not in request.FILES:
            return Response({"error": "CSV file not provided"}, status=400)

        file = request.FILES["file"]
        result = analyze_csv(file)

        return Response(result)


class GeneratePDFAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if "file" not in request.FILES:
            return Response({"error": "CSV file not provided"}, status=400)

        file = request.FILES["file"]
        result = analyze_csv(file)

        summary = {
            "total_count": result["total_count"],
            "avg_flowrate": result["avg_flowrate"],
            "avg_pressure": result["avg_pressure"],
            "avg_temperature": result["avg_temperature"],
            "type_distribution": result["type_distribution"],
        }

        pdf_path = generate_pdf_report(summary, result["table_data"])

        return FileResponse(
            open(pdf_path, "rb"),
            as_attachment=True,
            filename="equipment_report.pdf",
        )


# =========================================================
# HEALTH CHECK / HOME
# =========================================================
def home(request):
    return JsonResponse(
        {
            "status": "Backend is running",
            "project": "Chemical Equipment Parameter Visualizer",
            "backend": "Django + Django REST Framework",
        }
    )