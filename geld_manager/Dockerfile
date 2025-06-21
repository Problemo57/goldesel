FROM alpine:3.21.3

RUN apk add python3
RUN rm /usr/lib/python3*/EXTERNALLY-MANAGED
RUN python -m ensurepip

ADD / /
RUN pip3 install -r requirements.txt

EXPOSE 6868:6868/tcp

ENTRYPOINT sh ./start.sh
