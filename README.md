# Modular Data Transformer

A Python-based API for converting data between various formats (PDF, CSV, Excel, XML, JSON) with **API key authentication**, **usage logging**, and **monthly rate limiting**.

## Features

- **Multi-Format Conversions**  
  - **PDF → Excel** (with Tabula for table extraction)  
  - **CSV → JSON** / **CSV → Excel**  
  - **Excel → CSV** / **Excel → JSON**  
  - **JSON → CSV**  
  - **XML → JSON**  

- **API Key Authentication**  
  - Each user has a unique `X-API-Key`  
  - Stored in a SQLite `users` table  
  - Quick script for creating test users (`create_user.py`)

- **Usage Tracking & Rate Limiting**  
  - Logs each request in a `usage_log` table (timestamp, user, endpoint)  
  - Enforces monthly usage limit (e.g., 50 conversions)  
  - Returns `429` if limit is exceeded

- **Testing & Scripts**  
  - Comprehensive test suite (`pytest`) with 7 passing tests  
  - Scripts to generate test files (`create_test_csv.py`, `create_test_excel.py`, etc.)

- **Docker & Deployment** (optional next steps)  
  - Dockerize for easy deployment  
  - Deploy on cloud platforms (Heroku, AWS, etc.) or list on RapidAPI

## Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/<your-username>/modular-data-transformer.git
   cd modular-data-transformer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python app/core/init_db.py
   ```

## Usage

1. Create a user:
   ```bash
   python create_user.py my-secret-key 50
   ```
   This adds a user with API key `my-secret-key` and monthly limit of 50 requests.

2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Send a request:
   ```bash
   curl.exe -X POST "http://127.0.0.1:8000/convert/csv-to-json" ^
     -H "X-API-Key: my-secret-key" ^
     -F "file=@test_data.csv;type=text/csv"
   ```
   You should receive a JSON response with the converted CSV data.

## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss potential modifications.

## License

MIT
