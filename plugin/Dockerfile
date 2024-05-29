# Use a specific version for reproducibility
FROM python:3.10.12-slim

# Set environment variables
ENV PYTHONPATH=/code/ \
  PYTHONIOENCODING=utf-8 \
  API_RUN_ENV=docker \
  TERM=xterm-256color \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

# Install system dependencies and fonts
RUN apt-get update && apt-get install -y \
    fonts-noto \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy code to working directory
COPY ./app ./app
COPY ./bundles ./bundles
COPY ./bundle_dependency ./bundle_dependency
COPY ./config.py ./
COPY ./test ./test

# Command to run the application using gunicorn
CMD gunicorn --bind 0.0.0.0:8000 \
         --preload \
         --access-logfile - \
         --error-logfile - \
         --worker-connections 200 \
         -k uvicorn.workers.UvicornWorker \
         app.fastapi_app:app

EXPOSE 8000
