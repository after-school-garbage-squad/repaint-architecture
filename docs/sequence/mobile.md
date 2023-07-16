# イベント参加者アプリ

## シーケンス図(共通)

### func: 画像取得処理

```mermaid
sequenceDiagram
    participant app as 参加者
    participant back as バックエンドAPI
    participant img as 画像サーバー
    participant storage as 画像ストレージ
    app ->> back: 画像URLを要求(image id)
    back ->> img: one time url取得リクエスト(image id)
    img ->> img: one time urlを生成
    img -->> back: (one time url)
    back -->> app: (one time url)
    app ->> img: based on one time url
    img ->> img: one time url検証
    img ->> img: one time url更新
    img ->> storage: 画像取得(image_id)
    storage -->> img: (image raw)
    img -->> app: (image raw)

```

## シーケンス図(ケース)

### イベント参加時

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> app: 参加用QRコードスキャン
    app ->>+ back: (イベントQRのデータ,通知用ID)
    back ->> back: 参加者データ,UUID生成
    back ->> back: 参加者用QRコード作成
    back -->>- app: (イベントデータ,参加者データ)
    
```

### アプリ起動時(イベント参加以降)

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> back: (参加者識別データ,通知用ID)
    back -->> app: (イベントデータ,参加者データ)
    alt iOSなら
        back ->> app: (イベントの全てのビーコンデータ)
    end
    
```

### 画像選択

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    participant storage as 画像ストレージ
    app ->> back: 画像一覧リクエスト
    back -->> app: 画像データ一覧(urls)
    app ->> storage: func: 画像取得処理
    storage -->> app: 画像返却(raw)
    app ->> app: 画像一覧表示
    app ->> back: (選択した画像のID)
    back -->> app: (status)
    back ->> back: パレットに従ってあらかじめ画像合成を開始

```

### 画像表示

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    participant img as 画像サーバー
    participant storage as 画像ストレージ
    app ->>+ back: 選択中の画像リクエスト
    alt 画像が存在していないなら<基本的に事前に画像は生成しておく>
      back ->> back: 参加者の現在のパレット状況から画像を生成する
      back ->> img: 生成した画像を保存
      img ->> storage: (image raw)
    end
    back ->> img: one time urlリクエスト(image_id)
    img -->> back: (one time url)
    back -->>- app: パレットに応じて色付けた画像のurl(url)
    app ->> img: func: 画像取得処理
    img -->> app: 色付けされた画像を返す(raw image)
    alt 画像DL
        app ->> app: 画像を保存
    end
```

### スポット検知

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> app: ビーコン検知
    app ->> back: (ビーコンデータ)
    back ->> back: ドロップ処理
```

### ピック用QRコードスキャン

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

### 参加者用QRコード表示

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> back: QRコードリクエスト
    back ->> app: 参加者用QRコード(QRコード)
```

### 通知のON/OFF

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> back: 通知変更リクエスト
    back ->> back: 通知常件変更
```

### 参加者データ削除

```mermaid
sequenceDiagram
    participant app as 参加者アプリ
    participant back as バックエンドAPI
    app ->> back: 参加者データ削除リクエスト
    back ->> back: 参加者データ削除
```
