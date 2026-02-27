FROM alpine:latest

WORKDIR /home/app

RUN apk add --no-cache wget &&\
    wget https://dl.min.io/server/minio/release/linux-amd64/minio &&\
    chmod +x minio &&\
    mv minio /usr/local/bin &&\
    mkdir -p /data