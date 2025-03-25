from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_xml_to_json():
    xml_data = """<root><item>Alice</item><item>Bob</item></root>"""
    files = {"file": ("data.xml", xml_data, "application/xml")}
    resp = client.post("/convert/xml-to-json", files=files)

    assert resp.status_code == 200
    json_data = resp.json()
    # Check if parsed data matches expected structure
    assert json_data == {"root": {"item": ["Alice", "Bob"]}}
