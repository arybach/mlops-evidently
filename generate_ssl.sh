#!/usr/bin/env bash

set -eu
set -o pipefail

declare symbol=⠍

echo '[+] CA certificate and key'

if [ ! -f tls/certs/fastapi/ca/ca.key ]; then
    symbol=⠿

    mkdir -p tls/certs/fastapi/ca
    openssl genpkey -algorithm RSA -out tls/certs/fastapi/ca/ca.key
    openssl req -new -x509 -key tls/certs/fastapi/ca/ca.key -out tls/certs/fastapi/ca/ca.crt -days 3650 -subj "/CN=example-ca"

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

if [ ! -f tls/certs/streamlit/ca/ca.key ]; then
    symbol=⠿

    mkdir -p tls/certs/streamlit/ca
    openssl genpkey -algorithm RSA -out tls/certs/streamlit/ca/ca.key
    openssl req -new -x509 -key tls/certs/streamlit/ca/ca.key -out tls/certs/streamlit/ca/ca.crt -days 3650 -subj "/CN=example-ca"

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

declare ca_fingerprint
ca_fingerprint="$(openssl x509 -fingerprint -sha256 -noout -in tls/certs/fastapi/ca/ca.crt \
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
    openssl x509 -req -days 3650 -in tls/certs/fastapi/server/server.csr -CA tls/certs/fastapi/ca/ca.crt -CAkey tls/certs/fastapi/ca/ca.key -CAcreateserial -out tls/certs/fastapi/server/server.crt

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

if [ ! -f tls/certs/streamlit/server/server.key ]; then
    symbol=⠿

    mkdir -p tls/certs/streamlit/server
    openssl genpkey -algorithm RSA -out tls/certs/streamlit/server/server.key
    openssl req -new -key tls/certs/streamlit/server/server.key -out tls/certs/streamlit/server/server.csr -subj "/CN=example-server"
    openssl x509 -req -days 3650 -in tls/certs/streamlit/server/server.csr -CA tls/certs/streamlit/ca/ca.crt -CAkey tls/certs/streamlit/ca/ca.key -CAcreateserial -out tls/certs/streamlit/server/server.crt

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

declare server_fingerprint
while IFS= read -r file; do
    echo "   ${symbol}   ${file}"
done < <(find tls/certs/fastapi/server -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)

declare symbol=⠍

echo '[+] CA certificate and key'

if [ ! -f tls/certs/postgres/ca/ca.key ]; then
    symbol=⠿

    mkdir -p tls/certs/postgres/ca
    openssl genpkey -algorithm RSA -out tls/certs/postgres/ca/ca.key
    openssl req -new -x509 -key tls/certs/postgres/ca/ca.key -out tls/certs/postgres/ca/ca.crt -days 3650 -subj "/CN=example-ca"

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

declare ca_fingerprint
ca_fingerprint="$(openssl x509 -fingerprint -sha256 -noout -in tls/certs/postgres/ca/ca.crt \
    | cut -d '=' -f2 \
    | tr -d ':' \
    | tr '[:upper:]' '[:lower:]'
)"

echo "   ${symbol} SHA256 fingerprint: ${ca_fingerprint}"

while IFS= read -r file; do
    echo "   ${symbol}   ${file}"
done < <(find tls/certs/postgres/ca -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)

symbol=⠍

echo '[+] Server certificates and keys'

if [ ! -f tls/certs/postgres/server/server.key ]; then
    symbol=⠿

    mkdir -p tls/certs/postgres/server
    openssl genpkey -algorithm RSA -out tls/certs/postgres/server/server.key
    openssl req -new -key tls/certs/postgres/server/server.key -out tls/certs/postgres/server/server.csr -subj "/CN=example-server"
    openssl x509 -req -days 3650 -in tls/certs/postgres/server/server.csr -CA tls/certs/postgres/ca/ca.crt -CAkey tls/certs/postgres/ca/ca.key -CAcreateserial -out tls/certs/postgres/server/server.crt

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

while IFS= read -r file; do
    echo "   ${symbol}   ${file}"
done < <(find tls/certs/postgres/server -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)
