FROM python:3.9-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    aapt \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the script into the container
COPY apkparser.py /app/

# Set the working directory to /app
WORKDIR /app

# Set the entrypoint to the script
ENTRYPOINT ["python", "apkparser.py"]
