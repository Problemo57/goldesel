FROM debian:trixie-20250407-slim

ARG EARNAPP_ID
ENV EARNAPP_ID=$EARNAPP_ID

COPY hostnamectl /bin
RUN chmod +x /bin/hostnamectl

RUN mkdir -p /etc/earnapp
RUN echo -n "sdk-node-$(echo $EARNAPP_ID | md5sum | cut -d' ' -f1 -z)" > /etc/earnapp/uuid

RUN apt update && apt install -y wget
RUN wget -qO- https://brightdata.com/static/earnapp/install.sh > /tmp/earnapp.sh && bash /tmp/earnapp.sh -y

COPY start.sh /
RUN chmod +x /start.sh
ENTRYPOINT exec ./start.sh
HEALTHCHECK --interval=10s CMD ls -l /proc/$(pidof earnapp)/fd | cut -d' ' -f11- | tr -d '\n' | grep -q -v '/usr/bin/earnapp/dev/null/etc/earnapp/brd_sdk3.log'
