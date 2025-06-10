FROM python:3.13-bullseye

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instal gdal
RUN apt-get update && apt-get install -y gdal-bin

ENV PYTHONPATH=/app/src

ENTRYPOINT ["python", "src/ingest/run_ingest.py"]