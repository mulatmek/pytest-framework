# Use the requested Python version
FROM python:3.12-slim

WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and ensure it is executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# Set the default environment variable
ENV BASE_URL="http://default-hardcoded-url.com"

# This script will receive any arguments passed to 'docker run'
ENTRYPOINT ["/app/entrypoint.sh"]