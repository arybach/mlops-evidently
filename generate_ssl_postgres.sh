#!/usr/bin/env bash

set -eu
set -o pipefail

declare symbol=⠍

tls_dir="/scripts/tls"

echo '[+] CA certificate and key'

if [ ! -f "${tls_dir}/certs/postgres/ca.key" ]; then
    symbol=⠿

    mkdir -p "${tls_dir}/certs/postgres/ca"
    openssl genpkey -algorithm RSA -out "${tls_dir}/certs/postgres/ca.key"
    openssl req -new -x509 -key "${tls_dir}/certs/postgres/ca.key" -out "${tls_dir}/certs/postgres/ca.crt" -days 3650 -subj "/CN=example-ca"

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

declare ca_fingerprint
ca_fingerprint="$(openssl x509 -fingerprint -sha256 -noout -in "${tls_dir}/certs/postgres/ca.crt" \
    | cut -d '=' -f2 \
    | tr -d ':' \
    | tr '[:upper:]' '[:lower:]'
)"

echo "   ${symbol} SHA256 fingerprint: ${ca_fingerprint}"

while IFS= read -r file; do
    echo "   ${symbol}   ${file}"
done < <(find "${tls_dir}/certs/postgres/ca" -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)

symbol=⠍

echo '[+] Server certificates and keys'

if [ ! -f "${tls_dir}/certs/postgres/server/server.key" ]; then
    symbol=⠿

    mkdir -p "${tls_dir}/certs/postgres/server"
    openssl genpkey -algorithm RSA -out "${tls_dir}/certs/postgres/server/server.key"
    openssl req -new -key "${tls_dir}/certs/postgres/server/server.key" -out "${tls_dir}/certs/postgres/server/server.csr" -subj "/CN=example-server"
    openssl x509 -req -days 3650 -in "${tls_dir}/certs/postgres/server/server.csr" -CA "${tls_dir}/certs/postgres/ca.crt" -CAkey "${tls_dir}/certs/postgres/ca.key" -CAcreateserial -out "${tls_dir}/certs/postgres/server/server.crt"

    echo '   ⠿ Created'
else
    echo '   ⠍ Already present, skipping'
fi

while IFS= read -r file; do
    echo "   ${symbol}   ${file}"
done < <(find "${tls_dir}/certs/postgres/server" -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)
