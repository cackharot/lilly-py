FROM alpine:edge

MAINTAINER cackharot <cackharot@gmail.com>

RUN apk add --update python3 curl

RUN python3 -m ensurepip

RUN mkdir -p /opt/lilly

ADD ./ /opt/lilly

WORKDIR /opt/lilly

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD python3 __init__.py
