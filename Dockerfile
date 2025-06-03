FROM python:3.13-bullseye

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "ingest/run_ingest.py"]