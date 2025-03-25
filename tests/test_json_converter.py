from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_json_to_csv():
    data = [
        {"Name":"Alice","Age":30},
        {"Name":"Bob","Age":25}
    ]
    files = {
        "file": ("data.json", json.dumps(data), "application/json")
    }
    resp = client.post("/convert/json-to-csv", files=files)
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    csv_str = resp.content.decode()
    assert "Alice" in csv_str
    assert "Bob" in csv_str
