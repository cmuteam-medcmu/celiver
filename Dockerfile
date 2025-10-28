FROM python:3.12-slim 

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

# Default command (can be overridden)
# CMD ["python", "--version"]

# Example: your script entrypoint 
ENTRYPOINT ["python", "src/celiver.py"]