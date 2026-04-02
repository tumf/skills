# Python の探索シグナル

## 外部依存シグナル

- `requests.`
- `httpx.`
- `subprocess.`
- `os.environ`
- `datetime.now()` / `datetime.utcnow()`
- `time.sleep()`
- `pathlib.Path(...)` / `open(...)`
- DB client (`sqlalchemy`, `psycopg`, `redis`, `boto3` など)

## テスト側の注目点

- pytest test が本物のネットワークへ出ていないか
- monkeypatch なしで env や global state に依存していないか
- sleep を使って非同期完了待ちしていないか
- fixture が大きすぎて重複や責務不明瞭を生んでいないか

## よくある整理案

- repository / service 境界で fake を入れる
- clock を注入するか freezegun 相当で固定する
- subprocess 呼び出しを wrapper に閉じ込める
- DB 直結 test は pytest marker で integration 扱いを明示する
