import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader

def pdf_to_excel(pdf_bytes: bytes) -> bytes:
    reader = PdfReader(BytesIO(pdf_bytes))
    tables = []
    for page in reader.pages:
        try:
            df = pd.read_pdf(page.extract_text())
            tables.append(df)
        except Exception:
            continue

    if not tables:
        raise ValueError("No tables found")

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    for i, df in enumerate(tables):
        df.to_excel(writer, sheet_name=f"Page{i+1}", index=False)
    writer.save()
    return output.getvalue()

