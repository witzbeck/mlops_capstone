FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

# set PATH
ENV PATH="/root/.local/bin:${PATH}"

# copy assets over to image
COPY . /app

# set the working directory
WORKDIR /app

RUN pip3 install --user --no-cache-dir .

RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr && apt-get clean
