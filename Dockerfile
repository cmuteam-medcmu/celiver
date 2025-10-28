FROM python:3.12-alpine 

WORKDIR /app 

COPY . . 

RUN apk add --no-cache \
    build-base \
    gfortran \
    cmake \
    openblas-dev \
    libgomp \
    git \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del git cmake \
    && rm -rf /root/.cache

# Default command (can be overridden)
CMD ["python", "--version"]

# Example: your script entrypoint 
# ENTRYPOINT ["python", "src/celiver.py"]