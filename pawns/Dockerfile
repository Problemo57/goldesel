FROM iproyal/pawns-cli
FROM alpine:3.21.3
COPY --from=0 /pawns-cli /

ENV PAWNS_EMAIL=""
ENV PAWNS_PASSWORD=""
ENV PAWNS_DEVICE=""

COPY start.sh /
RUN chmod +x /start.sh
ENTRYPOINT exec /start.sh
