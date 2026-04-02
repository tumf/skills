# Go の探索シグナル

## 外部依存シグナル

- `http.Get(` / `http.Client`
- `time.Now()` / `time.Sleep()`
- `os.Getenv(`
- `os/exec`
- `os.Open` / `os.ReadFile`
- DB driver (`database/sql`, `pgx`, `redis`, etc.)

## テスト側の注目点

- interface を使わず具体実装へ直接結合していないか
- goroutine / retry / timeout が実時間依存で flaky になっていないか
- package-global state を跨いで order dependent になっていないか
- httptest で十分な箇所と本物ネットワークを混同していないか

## よくある整理案

- clock / runner / repository を interface 化する
- `httptest` や fake implementation で unit を安定化する
- DB を使うものは integration test として分離する
- table-driven test にまとめられる重複を圧縮する
