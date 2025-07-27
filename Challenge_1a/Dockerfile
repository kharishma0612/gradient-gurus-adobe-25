## FROM --platform=linux/amd64 python:3.10

# WORKDIR /app

# # Copy the processing script
# COPY process_pdfs.py .

# # Run the script
# CMD ["python", "process_pdfs.py"] 

FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install only required libraries
RUN pip install --no-cache-dir pymupdf

COPY process_pdfs.py .

CMD ["python", "process_pdfs.py"]
