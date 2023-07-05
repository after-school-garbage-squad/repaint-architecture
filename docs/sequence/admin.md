# イベント運営用コンソール

## 運営Web向けシーケンス図

### イベント作成

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->>+ back: Auth0ログイン
    back ->>- web: 認証
    web ->> web: イベント情報入力
    web ->>+ back: (イベントデータ)
    back ->>- back: イベント生成
    
```

### イベント更新

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->> web: イベント情報入力
    web ->> back: (イベントデータ)
    
```

### 運営アカウント追加

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant new as 新しい運営アカウント
    participant back as バックエンドAPI
    web ->>+ back: 追加したいメールアドレスを入力
    back  ->> back: メールアドレスをイベントDBに登録
    back ->>- new: 単純なシステムログインリンクをメールに送信
    new ->> back: Auth0でログイン
    back ->> back: イベントに所属していることを認識
    back -->> new: イベント一覧を返却
    
```

### スポット一覧

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->> back: スポット一覧のリクエスト
    back -->> web: (スポット一覧)
    
```

### スポット削除

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->> back: (スポットID)
    back -->> web: (status)
    
```

### スポットQR発行

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->>+ back: (スポットID)
    back ->> back: QRコード生成
    back -->>- web: QRコード画像(raw)
    
```

### 参加用イベントQR発行

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->>+ back: 参加者用QR発行リクエスト
    back ->> back: QRコード生成
    back -->>- web: QRコード画像(raw)
    
```

### 手動通知

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->>+ back: 通知リクエスト(通知内容)
    back ->> back: 当てはまるユーザーに通知
    back -->>- web: (status)
    
```

### 人流監視

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    loop
        web ->> back: ポーリング
        back -->> web: それぞれのスポットの参加者の状況
    end
```

### 人流制御

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->> back: POST(from, to)
    back --> back: 人流制御開始
    back -->> web: status
    
```

## 運営モバイル向けシーケンス図

### スポット登録

```mermaid
sequenceDiagram
    participant app as 運営用アプリ
    participant back as バックエンドAPI
    app ->>+ app: ビーコンスキャン
    app ->> app: スポット名入力
    app ->>- back: (ビーコンデータ)
    back ->> back: スポット登録
    back -->> app: (status)
    
```

### スポット確認

```mermaid
sequenceDiagram
    participant app as 運営用アプリ
    participant back as バックエンドAPI
    opt ビーコン
        app ->> app: ビーコンスキャン
        app ->> back: (ビーコンデータ)
        back -->> app: スポットデータ
    end
    opt QRコード
        app ->> app: QRスキャン
        app ->> back: (スポットデータ)
        back -->> app: スポットデータ
    end
    
```

### 写真撮影

```mermaid
sequenceDiagram
    participant app as 運営用アプリ
    participant back as バックエンドAPI
    app ->>+ app: 参加者QR読み取り
    app ->>+ back: 参加者データ
    back -->> app: 参加者確認(status)
    alt 参加者がすでに写真撮影をしていた
        app ->> app: 上書き確認
    end
    app ->> app: 写真撮影
    app ->> app: 写真確認
    app ->>- back: (画像raw)
    back -->>- app: (status)
    
```
