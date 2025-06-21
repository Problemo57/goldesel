FROM traffmonetizer/cli_v2:arm64v8
FROM traffmonetizer/cli_v2:latest
FROM alpine:3.21.3

RUN mkdir /app
COPY --from=0 /app/Cli /app/Cli_arm64
COPY --from=1 /app/Cli /app/Cli_amd64
ENV APP_UID=1654 ASPNETCORE_HTTP_PORTS=8080 DOTNET_RUNNING_IN_CONTAINER=true DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true
RUN apk add --upgrade --no-cache ca-certificates-bundle libgcc libssl3 libstdc++ zlib
RUN addgroup --gid=$APP_UID app && adduser --uid=$APP_UID --ingroup=app --disabled-password app
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1

COPY start.sh /
RUN chmod +x /start.sh

ENV TRAFFMONETIZER_TOKEN='fuhDWzSlm7v7EwM8AWdNtZh03aN2cu7Add0AMkmO+ig='
ENV TRAFFMONETIZER_DEVICE="sehnde"

ENTRYPOINT exec /start.sh
HEALTHCHECK CMD ping -w 2 "blnc.traffmonetizer.com"
