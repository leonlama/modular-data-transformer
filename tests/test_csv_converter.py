import io
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_csv_to_json():
    # Prepare a simple CSV string
    csv_data = "Name,Age\nAlice,30\nBob,25"
    files = {"file": ("data.csv", csv_data, "text/csv")}
    
    response = client.post("/convert/csv-to-json", files=files)
    assert response.status_code == 200
    
    # Expected result: a list of dictionaries
    expected = [{"Name": "Alice", "Age": 30}, {"Name": "Bob", "Age": 25}]
    json_data = response.json()
    assert json_data == expected

def test_csv_to_excel():
    # Prepare a simple CSV string
    csv_data = "Name,Age\nAlice,30\nBob,25"
    files = {"file": ("data.csv", csv_data, "text/csv")}
    
    response = client.post("/convert/csv-to-excel", files=files)
    assert response.status_code == 200
    # Verify the content type is for Excel
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in response.headers["content-type"]
    
    # Read the returned Excel bytes into a DataFrame
    excel_bytes = io.BytesIO(response.content)
    df = pd.read_excel(excel_bytes)
    
    # Create the expected DataFrame
    expected_df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})
    
    # Use pandas testing utility to compare DataFrames
    pd.testing.assert_frame_equal(df, expected_df)
