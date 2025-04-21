FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make script executable and set proper line endings
RUN chmod +x start.sh && \
    sed -i 's/\r$//' start.sh  # Remove Windows line endings if present

# Run the application
CMD ["./start.sh"]