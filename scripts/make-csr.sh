#!/usr/bin/env bash
# APNs 用 MDM プッシュ証明書の CSR を作る。出来た .csr を identity.apple.com に上げる。
set -euo pipefail

ORG="${ORG_NAME:-MDM}"
OUTDIR="${OUTDIR:-./mdm-certificates}"
mkdir -p "$OUTDIR"

openssl req -new -newkey rsa:2048 -nodes \
  -keyout "$OUTDIR/push.key" \
  -out "$OUTDIR/push.csr" \
  -subj "/CN=MDM Push Certificate/O=${ORG}"

echo "作成:"
echo "  秘密鍵: $OUTDIR/push.key   (絶対に流出させない)"
echo "  CSR   : $OUTDIR/push.csr   (Apple Push Certificates Portal にアップロード)"
