# Modular Data Transformer API

A Python-based SaaS API for automating PDFExcel and other data transformations.

## Getting Started

### Local

```bash
git clone https://github.com/leonlama/modular-data-transformer.git
cd modular-data-transformer
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

