# 汎用シーケンス

## 参加者

### 画像取得

```mermaid
sequenceDiagram
    participant app as 参加者
    participant back as バックエンドAPI
    participant img as 画像管理サーバー
    participant storage as 画像ストレージ
    app ->> back: 画像URLを要求(image id)
    back ->> back: idからurlに変換
    back ->> img: urlにトークンを付与
    img -->> back: (one time url)
    back -->> app: (one time url)
    app ->> img: based on one time url
    img ->> img: 色々認証
    img ->> storage: リバースプロキシとして取得
    storage -->> img: (image raw)
    img -->> app: (image raw)

```

## 運営

### [運営ログイン](../spec/overview/README.md#Auth0-によるログイン)

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    participant auth0 as Auth0
    web ->> auth0: Auth0ログイン
    auth0 ->> web: トークン
    web ->> back: トークン
    back ->> auth0: JWT検証
    auth0 ->> back: 認証情報

```

### [写真撮影](../spec/overview/README.md#写真撮影)

```mermaid
sequenceDiagram
    participant app as 運営用アプリ
    participant back as バックエンドAPI
    participant img as 画像管理サーバー
    participant storage as 画像ストレージ
    app ->> app: 参加者QR読み取り
    app ->> back: 参加者データ
    back -->> app: 参加者確認(status)
    alt 参加者がすでに写真撮影をしていた
        app ->> app: 上書き確認
    end
    app ->> app: 写真撮影
    app ->> app: 写真確認
    app ->> back: (画像raw)
    back ->> img: 画像アップロード(raw, image_id)
    img ->> storage: 画像保存(raw, image_id)
    back -->> app: (status)

```

### 画像アップロード

```mermaid
sequenceDiagram
    participant admin as 運営コンソール
    participant back as バックエンドAPI
    participant img as 画像管理サーバー
    participant pubsub as 画像クラスタリングPub/Sub
    participant cluster as 画像クラスタリングサーバー
    participant storage as 画像ストレージ
    admin ->> back: 画像をアップロード(image raw)
    back ->> img: 画像アップロードリクエスト(image raw)
    img ->> storage: 画像保存(image raw, image_id)
    img ->> pubsub: クラスタリングpub(image_id)
    pubsub ->> cluster: クラスタリングsub(image_id)
    cluster ->> cluster: クラスタリング
    cluster ->> storage: クラスタリング結果(clustered image, palette_id)
    cluster ->> img: クラスタリング結果通知(image_id, palette_id)
    img ->> img: one time urlの差し替え
    img ->> back: 画像の更新通知

```

- [画像の更新通知](#画像更新)

### 画像生成

```mermaid
sequenceDiagram
    participant back as バックエンドAPI
    participant img as 画像管理サーバー
    participant pubsub as 画像生成Pub/Sub
    participant gen as 画像生成サーバー
    participant storage as 画像ストレージ
    back ->> img: 画像生成・更新リクエスト(image_id, palette_id)
    img ->> pubsub: 画像生成pub(image_id)
    pubsub ->> gen: 画像生成sub(image_id)
    gen ->> gen: 画像生成
    gen ->> storage: 画像保存(image raw, image_id)
    gen ->> img: 画像生成結果通知(image_id)
    img ->> img: one time urlの差し替え
    img ->> back: 画像の更新通知

```

- [画像の更新通知](#画像更新)

### 画像更新

```mermaid
sequenceDiagram
    participant mobile as アプリ
    participant back as バックエンドAPI
    participant img as 画像処理サーバー
    participant storage as 画像ストレージ
    back ->> img: 画像処理リクエスト(image_id, palette_ids, visitor_id)
    img ->> img: 画像処理
    img ->> back: 画像更新通知(visitor_id)
    loop ポーリング
        mobile ->> back: 画像が最終確認時間から更新されているか
        opt 画像が更新されているなら
            mobile ->> back: 画像取得urlリクエスト(image_id)
            back -->> back: idからurlに変換
            mobile ->> storage: urlから画像を取得
        end
    end

```
