from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_test_pdf(filename="test_table.pdf"):
    # 1) Prepare a PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # 2) Define some sample table data
    data = [
        ["Name", "Department", "Salary"],
        ["Alice", "Engineering", "$100,000"],
        ["Bob", "Marketing", "$85,000"],
        ["Charlie", "Finance", "$90,000"],
        ["Diana", "Sales", "$95,000"],
    ]

    # 3) Build a Table object
    table = Table(data)

    # 4) Style the table
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),  # Header row background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),       # Header row text color
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
    ])
    table.setStyle(style)

    # 5) Optionally add a small title or paragraph
    styles = getSampleStyleSheet()
    title_paragraph = Paragraph("<b>Sample Employee Table</b>", styles["Title"])

    # 6) Build the PDF
    doc.build([title_paragraph, table])

if __name__ == "__main__":
    create_test_pdf()
    print("test_table.pdf has been created!")

