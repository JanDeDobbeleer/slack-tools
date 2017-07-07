FROM node:alpine

WORKDIR /api
COPY . /api

RUN apk add --no-cache python3 gcc musl-dev python3-dev libxml2 libxslt-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache && \
    yarn install && \
    pip3 install -r requirements.txt
