# Mocking Playbook

## 使い分け

### mock
相互作用の検証が主目的のときに使う。呼び出し回数や引数を確認したい場面向け。

### stub
決まった戻り値を返せば十分なときに使う。分岐やエラー処理を安定して通したい場面向け。

### fake
簡易実装を置きたいときに使う。インメモリ repository やローカル clock など、振る舞いをある程度保ちたい場面に向く。

## 原則

- unit test では外部依存を境界の外へ押し出す
- integration test では本物を使う範囲を明示する
- 時刻・乱数・環境変数・filesystem は軽視しない
- fake で十分なものを過剰に mock しない

## 優先順位

1. dependency injection できる境界を作る
2. pure unit では fake / stub / mock を使い分ける
3. adapter 層の結合確認は integration test 側に寄せる

## よくある改善案

- `Date.now()` / `time.Now()` / `SystemTime::now()` を clock abstraction 経由にする
- `fetch` / `requests` / `http.Client` / `reqwest` を adapter に閉じ込める
- `exec.Command` / `subprocess` / `Command` を runner interface 経由にする
- DB client を repository interface の後ろに隠す
