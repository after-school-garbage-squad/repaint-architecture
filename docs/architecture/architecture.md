# システム構成

## 概要

- クラウドは GCP を使用
- 基本的にすべてサーバレス設計
- 外部から叩く API は App Engine の Back-end API を必ず経由する
- 監視は Firebase Analytics や Cloud Monitoring でメトリクスを取得し、Grafana で可視化する

### システム構成図

![クラウド構成図](/imgs/gcp_architecture.png)

![サービス構成図](/imgs/service_architecture.png)
