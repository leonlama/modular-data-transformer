# Use an official Python image
FROM python:3.11-slim

# Install Java (OpenJDK) so tabula can run
RUN apt-get update && apt-get install -y default-jre && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Add a build argument to bust the cache
ARG CACHEBUST=2
COPY requirements.txt .

# Use the build argument so that this step is re-run when CACHEBUST changes
RUN echo "$CACHEBUST" && pip install --no-cache-dir --force-reinstall -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Start uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
