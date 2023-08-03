#!/usr/bin/env bash

set -eu
set -o pipefail

declare symbol=⠍

echo '[+] CA certificate and key'

if [ ! -f tls/certs/fastapi/ca.key ]; then
    symbol=⠿

    mkdir -p tls/certs/fastapi/ca
    openssl genpkey -algorithm RSA -out tls/certs/fastapi/ca.key
    openssl req -new -x509 -key tls/certs/fastapi/ca.key -out tls/certs/fastapi/ca.crt -days 3650 -subj "/CN=example-ca"

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

declare ca_fingerprint
ca_fingerprint="$(openssl x509 -fingerprint -sha256 -noout -in tls/certs/fastapi/ca.crt \
    | cut -d '=' -f2 \
    | tr -d ':' \
    | tr '[:upper:]' '[:lower:]'
)"

echo "   ${symbol} SHA256 fingerprint: ${ca_fingerprint}"

while IFS= read -r file; do
    echo "   ${symbol}   ${file}"
done < <(find tls/certs/fastapi/ca -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)

symbol=⠍

echo '[+] Server certificates and keys'

if [ ! -f tls/certs/fastapi/server/server.key ]; then
    symbol=⠿

    mkdir -p tls/certs/fastapi/server
    openssl genpkey -algorithm RSA -out tls/certs/fastapi/server/server.key
    openssl req -new -key tls/certs/fastapi/server/server.key -out tls/certs/fastapi/server/server.csr -subj "/CN=example-server"
    openssl x509 -req -days 3650 -in tls/certs/fastapi/server/server.csr -CA tls/certs/fastapi/ca.crt -CAkey tls/certs/fastapi/ca.key -CAcreateserial -out tls/certs/fastapi/server/server.crt

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

while IFS= read -r file; do
    echo "   ${symbol}   ${file}"
done < <(find tls/certs/fastapi/server -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)
