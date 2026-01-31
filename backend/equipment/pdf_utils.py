from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(summary):
    file_name = "equipment_report.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Chemical Equipment Analysis Report")

    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y -= 40
    c.drawString(50, y, f"Total Equipment: {summary['total_count']}")
    y -= 20
    c.drawString(50, y, f"Average Flowrate: {summary['avg_flowrate']:.2f}")
    y -= 20
    c.drawString(50, y, f"Average Pressure: {summary['avg_pressure']:.2f}")
    y -= 20
    c.drawString(50, y, f"Average Temperature: {summary['avg_temperature']:.2f}")

    y -= 40
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Equipment Type Distribution:")

    y -= 25
    c.setFont("Helvetica", 12)
    for k, v in summary["type_distribution"].items():
        c.drawString(70, y, f"{k}: {v}")
        y -= 20

    c.showPage()
    c.save()

    return file_name
