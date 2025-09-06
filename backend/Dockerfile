# syntax=docker/dockerfile:1
FROM python:3.10.5-alpine3.16

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    g++

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

WORKDIR /flask-app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    apk del .build-deps

COPY . ./

# ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD /wait && python3 -m flask run --host=0.0.0.0

EXPOSE 5000
