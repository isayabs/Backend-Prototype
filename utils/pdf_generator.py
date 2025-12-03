from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os

PDF_DIR = "static/pdfs/"

def generate_pdf(title, start_date, end_date, df, output_filename):
    os.makedirs(PDF_DIR, exist_ok=True)

    filepath = os.path.join(PDF_DIR, output_filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 60, title)

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Date Range: {start_date} to {end_date}")

    today = datetime.now().strftime("%B %d, %Y")
    c.drawString(50, height - 120, f"Report Generated: {today}")

    table_data = [df.columns.tolist()] + df.values.tolist()

    table = Table(table_data, colWidths=[(width - 100) / len(df.columns)] * len(df.columns))

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ('FONTSIZE', (0, 0), (-1, 0), 11),

        ('BOTTOMPADDING', (0, 0), (-1,0), 8),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    table.setStyle(style)

    table_width, table_height = table.wrap(0, 0)
    x = 50
    y = height - 160 - table_height

    table.drawOn(c, x, y)

    c.save

    return filepath