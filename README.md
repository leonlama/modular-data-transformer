# Modular Data Transformer API

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/workflow/status/leonlama/modular-data-transformer/CI)](https://github.comleonlama/modular-data-transformer/actions)

The **Modular Data Transformer API** is a comprehensive, cloud-ready, and scalable RESTful service for converting data between multiple formats. Built with FastAPI and powered by Celery for asynchronous processing, it supports conversions such as:

- **PDF → Excel**
- **CSV → JSON** and **CSV → Excel**
- **Excel → CSV** and **Excel → JSON**
- **XML → JSON**
- **JSON → CSV**

Additionally, the API features robust **API key authentication**, **usage logging**, and **monthly rate limiting**, making it ideal for both free and premium subscription models.

## Features

- **Multi-Format Data Conversions**
  - PDF → Excel (table extraction using Tabula)
  - CSV → JSON and CSV → Excel
  - Excel → CSV and Excel → JSON
  - XML → JSON
  - JSON → CSV

- **Asynchronous Processing**
  - Asynchronous endpoints powered by Celery and Redis for handling large or batch file conversions without blocking.
  - Poll task status with a dedicated endpoint.

- **Authentication & Usage Tracking**
  - API key authentication using the `X-API-Key` header.
  - SQLite-based usage logging with rate limiting (e.g., 50 conversions/month for free users).
  - Endpoints to check current usage.

- **Ready for Production**
  - Clean, modular codebase following best practices.
  - Comprehensive automated tests ensure reliability.
  - Dockerized for easy deployment.

## Installation

### Prerequisites

- Python 3.11+
- Redis server (for Celery broker and backend)
- Optional: Java (for PDF table extraction)

### Clone the Repository

```bash
git clone https://github.com/leonlama/modular-data-transformer.git
cd modular-data-transformer
```

### Create a virtual environment and install dependencies:  

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Initialize database

```bash
python app/core/init_db.py
```

### Create a test user

```bash
python create_user.py my-secret-key 50
```

## Running the API

### Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### Start the Celery Worker

```bash
celery -A celery_app.celery_app worker --pool=solo --loglevel=info
```

## API Endpoints

### Conversion Endpoints

| Conversion | Endpoint | Method |
|------------|----------|--------|
| PDF → Excel | `/convert/pdf-to-excel-async` | POST |
| CSV → JSON | `/convert/csv-to-json-async` | POST |
| CSV → Excel | `/convert/csv-to-excel-async` | POST |
| Excel → CSV | `/convert/excel-to-csv-async` | POST |
| Excel → JSON | `/convert/excel-to-json-async` | POST |
| XML → JSON | `/convert/xml-to-json-async` | POST |
| JSON → CSV | `/convert/json-to-csv-async` | POST |

### Usage and Task Status

| Operation | Endpoint | Method | Description |
|-----------|----------|--------|-------------|
| Check API Usage | `/account/usage` | GET | Returns the current monthly usage and the monthly limit for the authenticated user |
| Poll Task Status | `/account/task-status/{task_id}` | GET | Returns the status and result of an asynchronous conversion task |

## Example cURL Requests

### Enqueue a CSV → JSON Conversion Task

```bash
curl.exe -X POST "http://127.0.0.1:8000/convert/csv-to-json-async" -H "X-API-Key: my-secret-key" -F "file=@test_data.csv;type=text/csv"
```

### Check Task Status

```bash
curl.exe -X GET "http://127.0.0.1:8000/account/task-status/<task_id>" -H "X-API-Key: my-secret-key"
```

Replace `<task_id>` with the ID returned from the previous request.

## Deployment

The API is designed for easy deployment:

Docker: Use the provided Dockerfile to build a container.

Cloud: Deploy on platforms like AWS, GCP, Heroku, or list on RapidAPI for increased visibility and monetization.

## Documentation

For detailed API documentation, visit the automatically generated Swagger UI at:

```bash
http://127.0.0.1:8000/docs
```

## Contributing

Contributions are welcome! Please fork this repository, create a new branch for your feature or bugfix, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback, please contact me at leon.lamarca@yahoo.com
