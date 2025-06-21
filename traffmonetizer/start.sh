#! /bin/sh

if [ "$(uname -m)" = "x86_64" ]; then
    cp /app/Cli_amd64 /app/Cli
else
    cp /app/Cli_arm64 /app/Cli
fi
/app/Cli start accept statistics status --token "$TRAFFMONETIZER_TOKEN" --device-name "$TRAFFMONETIZER_DEVICE"
