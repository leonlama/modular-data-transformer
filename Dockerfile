# Use an official Python image
FROM python:3.11-slim

# Install Java (OpenJDK) so tabula can run
RUN apt-get update && apt-get install -y default-jre && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
# Force reinstall with --no-cache-dir to prevent cached wheels from interfering
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Start uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
