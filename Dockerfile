# Use official slim Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
