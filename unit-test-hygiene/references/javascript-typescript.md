# JavaScript / TypeScript の探索シグナル

## 外部依存シグナル

- `fetch(`
- `axios.`
- `node-fetch`
- `setTimeout(` / `setInterval(`
- `Date.now(` / `new Date(`
- `process.env`
- `child_process`
- `fs.` / `fs/promises`
- DB client (`prisma`, `knex`, `mongoose`, `pg`, `redis` など)

## テスト側の注目点

- Jest/Vitest の test が本物の API URL を叩いていないか
- fake timer を使わず実時間に依存していないか
- `beforeEach` / `afterEach` で shared state を汚していないか
- snapshot が実装詳細を過剰固定していないか

## よくある整理案

- HTTP client を wrapper/adapter に寄せる
- timer を fake timer で制御する
- process.env を helper で閉じる
- DB 直結 test を integration test へ移すか in-memory fake に寄せる
