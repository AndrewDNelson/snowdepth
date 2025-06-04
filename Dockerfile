FROM python:3.13-bullseye

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/src

ENTRYPOINT ["python", "src/ingest/run_ingest.py"]