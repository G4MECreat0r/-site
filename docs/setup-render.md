# Render セットアップ

1. Render → New → Blueprint → このリポジトリを選択（`render.yaml` を読む）
2. 環境変数を投入
   - `mdm`: `MICROMDM_SERVER_URL`（例 `https://mdm-xxxx.onrender.com`）、`SCEP_CHALLENGE`（任意の長い文字列）、`APNS_CERT_B64`、`APNS_KEY_B64`
   - `mdm-api`: `MICROMDM_URL`（`https://mdm-xxxx.onrender.com`）、`MICROMDM_API_KEY`（mdmと同値）、`CORS_ORIGIN`（`https://<user>.github.io`）
3. `base64 -w0 push.pem` / `base64 -w0 push.key` の出力を `*_B64` に貼る
4. `mdm` が起動したら `https://<mdm>/healthz` を確認

注意:
- 永続ディスクは有料プラン限定。無料だと再デプロイで登録が消える
- `MICROMDM_API_KEY` は両サービスで一致させる
- RenderのTLSはプロキシ側。MicroMDMはHTTPで `$PORT` を待ち受ける
