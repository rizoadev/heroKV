FROM alpine:3.10

RUN apk add --update \
    alpine-sdk

RUN apk add --update \--repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    rocksdb \
    rocksdb-dev \
    snappy \
    zlib \
    bzip2

RUN apk add --update --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
    gflags
    
RUN apk add --update \
    autoconf \
    g++ \
    gcc \
    make \
    pkgconf \
    py-zmq 
RUN apk add --no-cache python3 \
    python3-dev \
    build-base \
    git && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip

RUN pip3 install python-rocksdb sanic

RUN apk del python3-dev \
    build-base \
    git && \
    rm -r /root/.cache

WORKDIR /home

COPY ./ /home

CMD ["python3", "-u", "/home/app/init.py"]
