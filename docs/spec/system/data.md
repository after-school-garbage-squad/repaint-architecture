# システムの仕様 - データ

## QR コード

### LP/イベント参加兼用コード

`https://<LPのドメイン>/?event=<イベントID>`

### ピックスポットのパレット取得コード

```JSON
{
  "type": "object",
  "properties": {
    "event_id": {
      "type": "string"
    },
    "spot_id": {
      "type": "string"
    }
  },
  "required": ["event_id", "spot_id"]
}
```

### 参加者識別コード

```JSON
{
  "type": "object",
  "properties": {
    "event_id": {
      "type": "string"
    },
    "user_id": {
      "type": "string"
    }
  },
  "required": ["event_id", "user_id"]
}
```
