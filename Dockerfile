FROM python:3.13-bookworm

# Instal gdal
RUN apt-get update && apt-get install -y gdal-bin libgdal-dev libhdf4-alt-dev libhdf4-0 libhdf4-doc
# RUN apt-get update && apt-get install -y gdal-bin

# Set working directory
WORKDIR /app

# Copy requirements for build caching
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy code
COPY . /app

ENV PYTHONPATH=/app/src

ENTRYPOINT ["python", "-m", "src.main"]