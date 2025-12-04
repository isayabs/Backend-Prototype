from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import (
    Table, 
    TableStyle,
    Paragraph,
    Spacer,
    SimpleDocTemplate
)
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

PDF_DIR = "static/pdfs/"

def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont("Helvetica", 10)
    canvas.drawRightString(
        doc.pagesize[0] - 40,   
        20,  
        text             
    )

def add_date_header(story, date_str):
    header_table = Table([[date_str]], colWidths=["100%"])

    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 13),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 10))

def generate_pdf(title, start_date, end_date, df, output_filename, summary_text: str | None=None, grouped_by_date: dict | None = None):
    os.makedirs(PDF_DIR, exist_ok=True)
    filepath = os.path.join(PDF_DIR, output_filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1,12))

    story.append(Paragraph(f"Date Range: {start_date} to {end_date}", styles["Normal"]))
    today = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Report Generated: {today}", styles["Normal"]))
    story.append(Spacer(1, 12))

    if summary_text:
        story.append(Paragraph("Summary:", styles["Heading3"]))

        for line in summary_text.split("\n"):
            story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 12))

    if grouped_by_date:
        for date_value, df_day in grouped_by_date.items():
            date_str = date_value.strftime("%B %d, %Y")

            add_date_header(story, date_str)

            if "status" in df_day.columns:
                summary_line = (
                    f"Total: {len(df_day)} | "
                    f"ON: {df_day['status'].eq('ON').sum()} | "
                    f"OFF: {df_day['status'].eq('OFF').sum()}"
                )
            else:
                summary_line = f"Total Records: {len(df_day)}"

            story.append(Paragraph(summary_line, styles["Normal"]))
            story.append(Spacer(1, 10))
            
            table_data = [df_day.columns.tolist()] + df_day.values.tolist()
            num_cols = len(df_day.columns)
            available_width = letter[0] - (doc.leftMargin + doc.rightMargin)
            
            expected_cols = ["sensor_id", "sensor_name", "sensor_type", "status", "last_updated", "date"]
            if all(col in df_day.columns for col in expected_cols):
                col_widths = [
                    available_width * 0.12,  
                    available_width * 0.26,  
                    available_width * 0.18,  
                    available_width * 0.10,  
                    available_width * 0.22,
                    available_width * 0.12,  
                ]
            else:
                col_widths = [available_width / num_cols] * num_cols

            table = Table(table_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
            ]))

            story.append(table)
            story.append(Spacer(1, 20))

    else: 
        if df is not None and not df.empty:
            table_data = [df.columns.tolist()] + df.values.tolist()
        else:
            table_data = [["No data available for the selected range"]]    

        num_cols = len(table_data[0])
        available_width = letter[0] - (doc.leftMargin + doc.rightMargin) 

        expected_cols = ["sensor_id", "sensor_name", "sensor_type", "status", "last_updated", "date"]
        if all(col in df.columns for col in expected_cols):
            col_widths = [
                available_width * 0.12,  
                available_width * 0.26,  
                available_width * 0.18,  
                available_width * 0.10,  
                available_width * 0.22,
                available_width * 0.12,  
            ]
        else:
            col_widths = [available_width / num_cols] * num_cols

        table = Table(table_data, colWidths=col_widths)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        story.append(table)

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    return filepath