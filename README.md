# mdm-location-profile

構成プロファイルを配布して、端末の位置情報を自分で取得するミニMDM。

- `site/` … GitHub Pages。プロファイル配布と取得状況の表示
- `server/` … Render。MDM本体（MicroMDM）と位置照会API
- `profiles/` … プロファイル雛形

## セットアップ

1. `docs/push-cert.md` の手順でAPNs用MDMプッシュ証明書を取得
2. `render.yaml` をRenderのBlueprintとしてデプロイ（`docs/setup-render.md`）
3. GitHubの Variables / Secrets を設定
   - vars: `ORG_NAME` `MDM_SERVER_URL` `TOPIC` `ENROLL_URL`
   - secrets: `SCEP_CHALLENGE`
4. `site/config.js` の `MDM_API_BASE` と `MDM_TOKEN` を設定
5. mainにpush → Pagesがデプロイされる

## 使い方

`site/index.html` のURL（またはQR）を相手に送る → インストール → ダッシュボードで「取得」。

## 制約

- iOSのみ実用。Androidは別途アプリが必要（`docs/android.md`）
- 位置はポーリング型。端末がオンラインかつ位置情報ONが前提
- 非監督端末は相手がいつでもプロファイルを削除できる
- プッシュ証明書は1年で失効。更新必須
