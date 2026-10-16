#!/bin/sh
set -eu

: "${MICROMDM_SERVER_URL:?MICROMDM_SERVER_URL が必要}"
: "${MICROMDM_API_KEY:?MICROMDM_API_KEY が必要}"

mkdir -p /certs /var/db/micromdm/repo

# base64 の証明書をファイル化（Renderのシークレット運用向け）
[ -n "${APNS_CERT_B64:-}" ] && printf '%s' "$APNS_CERT_B64" | base64 -d > /certs/apns.pem
[ -n "${APNS_KEY_B64:-}"  ] && printf '%s' "$APNS_KEY_B64"  | base64 -d > /certs/apns.key

set -- serve \
  -server-url "$MICROMDM_SERVER_URL" \
  -api-key "$MICROMDM_API_KEY" \
  -http-addr ":${PORT:-9000}" \
  -config-path /var/db/micromdm \
  -filerepo /var/db/micromdm/repo

[ -n "${SCEP_CHALLENGE:-}" ] && set -- "$@" -scep-challenge "$SCEP_CHALLENGE"
[ -f /certs/apns.pem ] && set -- "$@" -apns-cert /certs/apns.pem
[ -f /certs/apns.key ] && set -- "$@" -apns-key /certs/apns.key

echo "[mdm] micromdm $*"
exec micromdm "$@"
