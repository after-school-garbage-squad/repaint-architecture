# イベント運営用コンソール

## 運営 Web 向けシーケンス図

### [イベント作成](../spec/overview/README.md#イベントの作成・設定)

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->> web: イベント情報入力
    web ->>+ back: (イベントデータ)
    back ->>- back: イベント生成

```

- [イベントデータ](../spec/system/data.md#イベントデータ)
- [イベント参加 QR](../spec/system/data.md#LP/イベント参加兼用コード)

### [イベント更新](../spec/overview/README.md#イベントの作成・設定)

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->> web: イベント情報入力
    web ->> back: (イベントデータ)

```

- [イベントデータ](../spec/system/data.md#イベントデータ)

### [運営アカウント追加](../spec/overview/README.md#イベント管理者の招待)

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant new as 新しい運営アカウント
    participant back as バックエンドAPI
    web ->>+ back: 追加したいメールアドレスを入力
    back ->> new: 招待専用のログインリンクをメールに送信
    new ->> back: Auth0でログイン
    back ->> back: ユーザー情報を登録
    back -->>- new: イベント一覧を返却

```

### [スポットの設定](../spec/overview/README.md#スポットの詳細設定)

スポット名の変更・ピックの切り替え・スポットの削除・QR の発行を行う

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->> back: スポット一覧リクエスト
    back -->> web: (スポット一覧)
    web ->> web: スポットの設定
    web ->> web: ピック用QRコードの取得
    web ->> back: (スポットデータ)

```

- [スポットデータ](../spec/system/data.md#スポット)
- [ピック用 QR コード](../spec/system/data.md#ピックスポットのパレット取得コード)

### [人流監視](../spec/overview/README.md#人流制御)

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    loop
        web ->> back: ポーリング
        back -->> web: それぞれのスポットの参加者の状況
    end
```

- [スポットの状況](../spec/system/data.md#スポットのイベントログ)

### [人流制御](../spec/overview/README.md#人流制御)

```mermaid
sequenceDiagram
    participant web as 運営コンソール
    participant back as バックエンドAPI
    web ->> back: POST(from, to)
    back --> back: 人流制御開始
    back -->> web: status

```
