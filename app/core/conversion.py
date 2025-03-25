import tabula
import pandas as pd
from io import BytesIO

def pdf_to_excel(pdf_bytes: bytes) -> bytes:
    # Save PDF bytes to a temp file
    with open("temp.pdf", "wb") as f:
        f.write(pdf_bytes)

    # Extract all tables from every page
    tables = tabula.read_pdf("temp.pdf", pages="all", multiple_tables=True)

    if not tables:
        raise ValueError("No tables found")

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for idx, df in enumerate(tables):
            df.to_excel(writer, sheet_name=f"Page{idx+1}", index=False)
    return output.getvalue()
