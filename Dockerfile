FROM python:3.13-bullseye

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instal gdal
RUN apt-get update && apt-get install -y gdal-bin libgdal-dev libhdf4-alt-dev libhdf4-0 libhdf4-doc

ENV PYTHONPATH=/app/src

ENTRYPOINT ["python", "src/ingest/run_ingest.py"]