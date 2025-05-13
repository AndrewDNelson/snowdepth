FROM python:3.11-bullseye

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "ingest/snodas_download.py"]
