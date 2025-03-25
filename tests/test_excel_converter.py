from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
import io

client = TestClient(app)

def test_excel_to_csv():
    # Create an in-memory Excel file
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})
    excel_bytes = io.BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    # Send as a file
    files = {
        "file": ("data.xlsx", excel_bytes.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }
    resp = client.post("/convert/excel-to-csv", files=files)

    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    csv_content = resp.content.decode("utf-8")
    assert "Alice" in csv_content
    assert "Bob" in csv_content
