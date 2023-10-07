# イベント参加者アプリ

## シーケンス図(共通)

### func: 画像取得処理

[運営用 Web コンソールのシーケンス図を参照](common.md#画像取得処理)

## イベント参加者のシーケンス

### [イベント参加時](../spec/overview/README.md#イベント参加-QR-Sスキャン)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> app: イベント参加用QRコードスキャン
    app ->>+ back: イベント参加(イベントQRのデータ,通知用ID)
    back ->> back: 参加者データ,UUID生成
    back ->> back: 参加者識別QRコード事前作成
    back -->>- app: (イベントデータ,参加者データ)

```

- QR コード
  - [LP/イベント参加兼用コード](../spec/system/data.md#lpイベント参加兼用コード)
  - [参加者識別コード](../spec/system/data.md#参加者識別コード)
- [イベントデータ](../spec/system/data.md#イベントデータ)
- [参加者データ](../spec/system/data.md#参加者アカウントのデータ)

### [アプリ起動時(イベント参加以降)](../spec/overview/README.md#アプリ起動時の更新)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> back: (参加者識別データ,通知用ID)
    back -->> app: (イベントデータ,参加者データ,ビーコンデータ)

```

- [参加者識別データ(コードの JSON を流用)](../spec/system/data.md#参加者識別コード)
- [イベントデータ](../spec/system/data.md#イベントデータ)
- [参加者データ](../spec/system/data.md#参加者アカウントのデータ)
- [ビーコンデータ](../spec/system/data.md#ビーコン)

### [スポット検知](../spec/overview/README.md#スポット検知)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> app: ビーコン検知
    app ->> back: (ビーコンデータ)
    back ->> back: 色々な処理
    alt ピック可能なスポットなら
      app ->> app: 通知
    end
```

- [ビーコンデータ](../spec/system/data.md#ビーコン)

### [ピック用 QR コードスキャン](../spec/overview/README.md#ピック用-QR-スキャン)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> app: QRコードスキャン
    app ->>+ back: (ピック用QRコードデータ)
    alt QRコードと現在参加者がいるスポットが対応しているなら
      back ->> back: ピック処理
      back ->>- back: あらかじめ参加者のパレット状況に応じて画像合成
    end
```

- [ピックスポットのパレット取得コード](../spec/system/data.md#ピックスポットのパレット取得コード)

### 画像選択

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    participant storage as 画像ストレージ
    app ->> back: 画像一覧リクエスト
    back ->> storage: トークン生成リクエスト
    storage -->> back: (トークン)
    back -->> app: 画像(url)の一覧返却
    loop 全ての画像に対して
        app ->> storage: func: 画像取得処理
        storage ->> storage: 認証
        storage -->> app: 画像返却(raw)
    end
    app ->> app: 画像一覧表示
    app ->> back: (選択した画像のpublic ID)
    back -->> app: (status)
    back ->> back: パレットに従ってあらかじめ画像合成を開始

```

### [画像表示](../spec/overview/README.md#画像を表示)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    participant img as 画像管理サーバー
    participant storage as 画像ストレージ
    app ->>+ back: 選択中の画像リクエスト
    alt 画像が存在していないなら
      back ->> back: 画像を生成
      back ->> storage: 生成した画像を保存
    end
    back ->> img: one time urlリクエスト(image_id)
    img -->> back: (one time url)
    back -->>- app: パレットに応じて色付けた画像のurl(url)
    app ->> img: func: 画像取得処理
    img -->> app: 色付けされた画像を返す(png)
    alt 画像DL
        app ->> app: 画像を保存
    end
```

### 画像一覧取得

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    participant img as 画像管理サーバー
    app ->>+ back: 画像一覧リクエスト
    loop 画像
      back ->> back: 画像を生成
    end
    back -->>- app: 画像一覧返却(ids)
    app ->> img: func: 画像取得処理
    img -->> app: 色付けされた画像を返す(png)
```

### [参加者用 QR コード表示](../spec/overview/README.md#参加者-QR-表示)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    app ->> app: 参加者用QRコード生成
```

- [参加者用 QR コード](../spec/system/data.md#参加者識別コード)

### [通知の受信](../spec/overview/README.md#通知)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    participant fcm as FCM
    back ->> fcm: 通知送信(通知用ID,通知内容)
    fcm -->> app: 通知
```

### [参加者データ削除](../spec/overview/README.md#アカウントの削除)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> back: 参加者データ削除リクエスト
    back ->> back: 参加者データ削除
```

## イベント運営のシーケンス

[モバイル・コンソール共通の運営シーケンス](common.md#運営)

### [ビーコン・スポットの登録](../spec/overview/README.md#ビーコン・スポットの登録)

```mermaid
sequenceDiagram
    participant beacon as ビーコン
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> app: スポット登録処理開始
    beacon ->> app: (ビーコンデータ)
    app ->> app: スポット名の入力
    app ->> back: (スポット名,ビーコンデータ)
```

- [ビーコンデータ](../spec/system/data.md#ビーコン)

### [スポットの確認](../spec/overview/README.md#スポットの確認)

```mermaid
sequenceDiagram
    participant beacon as ビーコン
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    opt ビーコン
        app ->> app: スキャン開始
        beacon ->> app: (ビーコンデータ)
        app ->> back: (ビーコンデータ)
        back ->> app: (スポットデータ)
        app ->> app: 表示
    end
    opt QRコード
        app ->> beacon: QRスキャン
        beacon -->> app: (ピック用QRコードデータ)
        app ->> back: (スポットデータ)
        back -->> app: スポットデータ
    end
```

- [ビーコンデータ](../spec/system/data.md#ビーコン)
- [スポットデータ](../spec/system/data.md#スポット)
- [ピック用 QR コードデータ](../spec/system/data.md#ピックスポットのパレット取得コード)
