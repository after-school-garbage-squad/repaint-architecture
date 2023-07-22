# システム構成

## 概要

- クラウドはGCPを使用
- 基本的にすべてサーバレス設計
- 外部から叩くAPIはApp EngineのBack-end APIを必ず経由する
- 監視はFirebase AnalyticsやCloud Monitoringでメトリクスを取得し、Grafanaで可視化する

### システム構成図

![クラウド構成図](/imgs/gcp_architecture.png.png)
