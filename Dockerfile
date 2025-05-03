FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set PYTHONPATH to include the current directory
ENV PYTHONPATH=/app

CMD ["python", "run.py"] 