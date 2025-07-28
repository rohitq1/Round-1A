# Dockerfile
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app

# Create schema folder
RUN mkdir -p /app/schema

# Copy Python script and schema file
COPY process_pdfs.py /app/
COPY output_schema.json /app/schema/output_schema.json

# Install dependencies
RUN pip install --no-cache-dir pdfminer.six jsonschema

# Run script
CMD ["python", "process_pdfs.py"]
