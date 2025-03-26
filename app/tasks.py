# app/tasks.py
import io
import json
import base64
import pandas as pd
import tabula
import xmltodict
from celery_app import celery_app

@celery_app.task(name="app.tasks.csv_to_json_task")
def csv_to_json_task(encoded_file_bytes):
    """
    Converts CSV bytes to a JSON string asynchronously.
    """
    try:
        file_bytes = base64.b64decode(encoded_file_bytes)
        data = pd.read_csv(io.BytesIO(file_bytes))
        result = data.to_dict(orient="records")
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task(name="app.tasks.csv_to_excel_task")
def csv_to_excel_task(encoded_file_bytes):
    """
    Converts CSV bytes to Excel bytes asynchronously.
    The Excel file bytes are base64 encoded.
    """
    try:
        file_bytes = base64.b64decode(encoded_file_bytes)
        df = pd.read_csv(io.BytesIO(file_bytes))
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        output.seek(0)
        excel_bytes = output.getvalue()
        encoded = base64.b64encode(excel_bytes).decode("utf-8")
        return encoded
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task(name="app.tasks.excel_to_csv_task")
def excel_to_csv_task(encoded_file_bytes):
    """
    Converts Excel bytes to CSV string asynchronously.
    """
    try:
        file_bytes = base64.b64decode(encoded_file_bytes)
        df = pd.read_excel(io.BytesIO(file_bytes))
        csv_str = df.to_csv(index=False)
        return csv_str
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task(name="app.tasks.excel_to_json_task")
def excel_to_json_task(encoded_file_bytes):
    """
    Converts Excel bytes to JSON string asynchronously.
    """
    try:
        file_bytes = base64.b64decode(encoded_file_bytes)
        df = pd.read_excel(io.BytesIO(file_bytes))
        result = df.to_dict(orient="records")
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task(name="app.tasks.pdf_to_excel_task")
def pdf_to_excel_task(encoded_file_bytes):
    """
    Converts PDF file bytes to Excel bytes asynchronously.
    The Excel file bytes are base64 encoded.
    """
    try:
        file_bytes = base64.b64decode(encoded_file_bytes)
        # Create a BytesIO stream for PDF processing
        pdf_file = io.BytesIO(file_bytes)
        # Extract tables using tabula (assumes Java and tabula are properly set up)
        dfs = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
        if not dfs:
            raise Exception("No tables found in PDF")
        # Combine all tables into one DataFrame
        df = pd.concat(dfs, ignore_index=True)
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        excel_buffer.seek(0)
        excel_bytes = excel_buffer.getvalue()
        encoded = base64.b64encode(excel_bytes).decode("utf-8")
        return encoded
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task(name="app.tasks.xml_to_json_task")
def xml_to_json_task(encoded_file_bytes):
    """
    Converts XML bytes to a JSON string asynchronously.
    """
    try:
        file_bytes = base64.b64decode(encoded_file_bytes)
        xml_str = file_bytes.decode("utf-8")
        parsed = xmltodict.parse(xml_str)
        return json.dumps(parsed)
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task(name="app.tasks.json_to_csv_task")
def json_to_csv_task(encoded_file_bytes):
    """
    Converts JSON bytes to CSV string asynchronously.
    Expects JSON data to be a list of objects or a single object.
    """
    try:
        file_bytes = base64.b64decode(encoded_file_bytes)
        data = json.loads(file_bytes.decode("utf-8"))
        if isinstance(data, dict):
            data = [data]
        df = pd.DataFrame(data)
        csv_str = df.to_csv(index=False)
        return csv_str
    except Exception as e:
        return json.dumps({"error": str(e)})
