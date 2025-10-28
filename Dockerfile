FROM python:3.11-slim 

ARG VERSION=1.0.0
LABEL version=$VERSION

WORKDIR /app 

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    cmake \
    libopenblas-dev \
    libgomp1 \
    git \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove --purge -y git cmake \
    && rm -rf /root/.cache

COPY . . 

# Entrypoint 
ENTRYPOINT ["python", "src/celiver.py"]