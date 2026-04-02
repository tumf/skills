# Rust の探索シグナル

## 外部依存シグナル

- `reqwest`
- `std::process::Command`
- `tokio::time::sleep` / `std::thread::sleep`
- `SystemTime::now` / `Instant::now`
- `std::env::var`
- `std::fs`
- DB client (`sqlx`, `diesel`, `redis`, etc.)

## テスト側の注目点

- trait 境界なしで外部依存へ直接つながっていないか
- async test が実時間 sleep に依存していないか
- tempdir や env の扱いが cross-platform に不安定でないか
- integration test と unit test の責務が混ざっていないか

## よくある整理案

- trait と fake 実装で unit test を安定化する
- clock / command runner / repository を注入可能にする
- DB や HTTP adapter は integration test 側へ寄せる
- table-based / macro-based に圧縮できる重複を整理する
