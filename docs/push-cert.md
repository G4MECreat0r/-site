# APNs プッシュ証明書

1. `make csr`（`mdm-certificates/push.csr` と `push.key` が出来る）
2. https://identity.apple.com/pushcert にApple IDでログイン
3. 「Create a Certificate」→ CSRをアップロード → `push.pem` をダウンロード
4. Topic を確認（MDMペイロードに必要）
