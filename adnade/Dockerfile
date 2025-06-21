FROM alpine:3.21.3

ENV USERAGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
ENV USERNAME="problemo"
ENV PYTHONUNBUFFERED=1

RUN apk add python3
RUN rm /usr/lib/python3*/EXTERNALLY-MANAGED
RUN python -m ensurepip
RUN pip3 install requests
RUN echo 0 > health.txt

COPY adnade.py /
ENTRYPOINT exec python3 /adnade.py
HEALTHCHECK --interval=10s CMD if [ $(date +%s) -gt $(cat health.txt) ]; then exit 1; fi
