#!/usr/bin/env bash

set -eu
set -o pipefail

echo '[+] CA certificate and key'

if [ ! -f tls/certs/ca/ca.key ]; then
	mkdir -p tls/certs/ca  # Create the directory if not exists
	openssl genpkey -algorithm RSA -out tls/certs/ca/ca.key  # Generate CA private key
	openssl req -new -x509 -sha256 -key tls/certs/ca/ca.key -out tls/certs/ca/ca.crt -days 3650 -subj "/CN=MyLocalCA"  # Generate CA certificate
	echo '   ⠿ Created'
else
	echo '   ⠍ Already present, skipping'
fi

declare ca_fingerprint
ca_fingerprint="$(openssl x509 -fingerprint -sha256 -noout -in tls/certs/ca/ca.crt \
	| cut -d '=' -f2 \
	| tr -d ':' \
	| tr '[:upper:]' '[:lower:]'
)"

echo "   SHA256 fingerprint: ${ca_fingerprint}"

while IFS= read -r file; do
	echo "   ${file}"
done < <(find tls/certs/ca -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)

echo '[+] Server certificates and keys'

if [ ! -f tls/certs/server/server.key ]; then
	mkdir -p tls/certs/server  # Create the directory if not exists
	openssl genpkey -algorithm RSA -out tls/certs/server/server.key  # Generate server private key
	openssl req -new -sha256 -key tls/certs/server/server.key -out tls/certs/server/server.csr -subj "/CN=server"  # Generate server CSR
	openssl x509 -req -sha256 -in tls/certs/server/server.csr -CA tls/certs/ca/ca.crt -CAkey tls/certs/ca/ca.key -CAcreateserial -out tls/certs/server/server.crt -days 3650  # Sign server certificate with CA
	echo '   ⠿ Created'
else
	echo '   ⠍ Already present, skipping'
fi

while IFS= read -r file; do
	echo "   ${file}"
done < <(find tls/certs/server -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)
