import pandas as pd
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import UploadHistory

# 🔒 AUTH ADDITION (REQUIRED)
from rest_framework.exceptions import AuthenticationFailed

# 🔒 AUTH ADDITION (REQUIRED)
API_KEY = "demo-intern-key-123"

# 🔒 AUTH ADDITION (REQUIRED)
def check_api_key(request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        raise AuthenticationFailed("Invalid or missing API key")


@api_view(["POST"])
def upload_csv(request):
    # 🔒 AUTH ADDITION (REQUIRED)
    check_api_key(request)

    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    try:
        df = pd.read_csv(file)
    except Exception:
        return Response({"error": "Invalid CSV file"}, status=400)

    # ✅ FIX: normalize column names (IMPORTANT)
    df.columns = df.columns.str.replace(" ", "").str.strip()

    required_columns = [
        "EquipmentName",
        "Type",
        "Flowrate",
        "Pressure",
        "Temperature",
    ]

    for col in required_columns:
        if col not in df.columns:
            return Response(
                {"error": f"Missing column: {col}"},
                status=400,
            )

    summary = {
        "total_equipment": int(len(df)),
        "avg_flowrate": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict(),
    }

    UploadHistory.objects.create(
        filename=file.name,
        total_equipment=summary["total_equipment"],
        avg_flowrate=summary["avg_flowrate"],
        avg_pressure=summary["avg_pressure"],
        avg_temperature=summary["avg_temperature"],
    )

    # keep only last 5 uploads
    if UploadHistory.objects.count() > 5:
        UploadHistory.objects.order_by("uploaded_at").first().delete()

    preview = df.to_dict(orient="records")

    return Response({
        "summary": summary,
        "preview": preview,
    })


@api_view(["GET"])
def upload_history(request):
    # 🔒 AUTH ADDITION (REQUIRED)
    check_api_key(request)

    history = UploadHistory.objects.order_by("-uploaded_at")[:5]
    return Response([
        {
            "filename": h.filename,
            "uploaded_at": h.uploaded_at,
            "total_equipment": h.total_equipment,
            "avg_flowrate": h.avg_flowrate,
            "avg_pressure": h.avg_pressure,
            "avg_temperature": h.avg_temperature,
        }
        for h in history
    ])


@api_view(["GET"])
def generate_pdf_report(request):
    # 🔒 AUTH ADDITION (REQUIRED)
    check_api_key(request)

    latest = UploadHistory.objects.order_by("-uploaded_at").first()
    if not latest:
        return Response({"error": "No data available"}, status=400)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="equipment_report.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    y = 800

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Chemical Equipment Parameter Visualizer Report")

    c.setFont("Helvetica", 12)
    y -= 40
    c.drawString(50, y, f"File Name: {latest.filename}")
    y -= 25
    c.drawString(50, y, f"Total Equipment: {latest.total_equipment}")
    y -= 20
    c.drawString(50, y, f"Average Flowrate: {latest.avg_flowrate:.2f}")
    y -= 20
    c.drawString(50, y, f"Average Pressure: {latest.avg_pressure:.2f}")
    y -= 20
    c.drawString(50, y, f"Average Temperature: {latest.avg_temperature:.2f}")

    c.showPage()
    c.save()
    return response




