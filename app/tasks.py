# app/tasks.py
import io
import json
import pandas as pd
import tabula
import xmltodict
from celery_app import celery_app

@celery_app.task
def csv_to_json_task(file_bytes):
    """
    Converts CSV bytes to JSON string asynchronously.
    """
    try:
        # Decode the bytes (assuming UTF-8 encoding)
        data = pd.read_csv(io.BytesIO(file_bytes))
        result = data.to_dict(orient="records")
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task
def csv_to_excel_task(file_bytes):
    """
    Converts CSV to Excel asynchronously.
    :param file_bytes: binary CSV data.
    :return: Excel file bytes.
    """
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        return {"error": str(e)}

@celery_app.task
def excel_to_csv_task(file_bytes):
    """
    Converts Excel bytes to CSV string asynchronously.
    :param file_bytes: binary Excel data.
    :return: CSV string.
    """
    try:
        df = pd.read_excel(io.BytesIO(file_bytes))
        csv_str = df.to_csv(index=False)
        return csv_str
    except Exception as e:
        return {"error": str(e)}

@celery_app.task
def excel_to_json_task(file_bytes):
    """
    Converts Excel bytes to JSON string asynchronously.
    :param file_bytes: binary Excel data.
    :return: JSON string.
    """
    try:
        df = pd.read_excel(io.BytesIO(file_bytes))
        result = df.to_dict(orient="records")
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task
def pdf_to_excel_task(file_bytes):
    """
    Converts PDF file bytes to Excel.
    :param file_bytes: binary PDF data.
    :return: Excel file bytes.
    """
    try:
        # Save PDF bytes to temporary file that tabula can read
        pdf_file = io.BytesIO(file_bytes)
        
        # Extract tables from PDF using tabula
        dfs = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
        
        # Combine all tables into one dataframe
        df = pd.concat(dfs, ignore_index=True)
        
        # Convert to Excel bytes
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        excel_bytes = excel_buffer.getvalue()
        
        return excel_bytes
        
    except Exception as e:
        return {"error": str(e)}

@celery_app.task
def xml_to_json_task(file_bytes):
    """
    Asynchronously converts XML bytes to a JSON string.
    """
    try:
        # Decode bytes to string (assumes UTF-8 encoding)
        xml_str = file_bytes.decode("utf-8")
        # Parse XML into an OrderedDict
        parsed = xmltodict.parse(xml_str)
        # Return the JSON string
        return json.dumps(parsed)
    except Exception as e:
        return json.dumps({"error": str(e)})

@celery_app.task
def json_to_csv_task(file_bytes):
    """
    Asynchronously converts JSON bytes to a CSV string.
    Expects the JSON data to be a list of objects or a single object.
    """
    try:
        # Decode the bytes (assuming UTF-8)
        data = json.loads(file_bytes.decode("utf-8"))
        
        # If it's a single dict, wrap it in a list
        if isinstance(data, dict):
            data = [data]
        
        # Convert to DataFrame and then to CSV
        df = pd.DataFrame(data)
        csv_str = df.to_csv(index=False)
        return csv_str
    except Exception as e:
        # Return error message in JSON format if something goes wrong
        return json.dumps({"error": str(e)})
