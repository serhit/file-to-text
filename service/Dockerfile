FROM python:3.8-slim

# Install basic requirements for application
RUN apt-get update && \
    apt-get install -y antiword unrtf poppler-utils && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

RUN pip install --no-cache-dir \
	uvicorn==0.17.6 \
	fastapi==0.75.2 \
	python-multipart==0.0.5 \
	textract

# Install applicaiton

RUN mkdir /app
WORKDIR /app/
COPY *.py /app/

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "main:app"]

EXPOSE 8000
