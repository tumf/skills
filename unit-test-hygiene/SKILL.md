---
name: unit-test-hygiene
description: |
  Audit and reorganize an existing test suite to remove outdated tests, reduce duplication, and isolate external dependencies from unit tests.
  Use this skill whenever the user wants to clean up tests, find obsolete or redundant tests, detect unit tests that directly hit APIs/URLs/timers/commands/databases/filesystems/env state, improve mock boundaries, reduce flakiness, or clarify the boundary between unit and integration tests. Use it even if the user only says things like "整理したい", "モック化したい", "テストが遅い", or "古いテストを掃除したい".
---

# unit-test-hygiene

既存のテストスイートを棚卸しし、不要・重複・冗長・外部依存の混入を整理するためのスキルです。

このスキルの仕事は、単に「モックを増やす」ことではありません。価値があるのは、**どのテストを残し、どれを削り、どれを統合し、どこに境界を引くべきか**を説明可能な形で整理することです。

## このスキルが扱うこと

- 古い仕様・廃止機能にぶら下がった不要テストの発見
- 重複・冗長・過剰に実装詳細へ依存したテストの整理
- API / URL / timer / clock / command / DB / filesystem / env などの外部依存を直接利用しているテストの検出
- unit test と integration test の境界の見直し
- mock / stub / fake / dependency injection の方針提案
- flaky になりやすいテストのシグナル抽出

## 基本姿勢

- まず調査し、分類し、根拠を示す。
- いきなり削除しない。**削除候補**として扱い、なぜ削除してよいのかを説明する。
- いきなり「全部モック化」しない。unit test では隔離し、integration test や contract test では残す価値を判断する。
- 実装詳細の一致より、振る舞いの価値と保守コストを見る。
- テストの数ではなく、信頼性・意図の明瞭さ・変更耐性を改善する。

## ワークフロー

### 1. テストスイートの棚卸し

最初に以下を把握する。

- どのテストフレームワークを使っているか
- どこに test / spec / integration / e2e があるか
- 主要な外部依存は何か
- deprecated / legacy / obsolete / unused を示すシグナルがどこにあるか
- 本番コード側に、依存注入や adapter 境界がすでにあるか

必要に応じて以下を読む。

- `README.md`
- `docs/`
- テスト設定ファイル（例: jest, vitest, pytest, go test, cargo test 周辺）
- 主要な test ディレクトリ
- 外部依存を持つ production code

### 2. テストを分類する

各テスト、またはテスト群を次の観点で分類する。

#### A. 生存性

- **現役**: 現在の仕様・公開 API・現在の振る舞いを守っている
- **要確認**: 古い仕様の名残かもしれないが、即削除は危険
- **削除候補**: すでに存在しない機能や旧仕様のみを固定している

#### B. 重複度

- **明確な重複**: 同じ振る舞いをほぼ同じ入力・期待値で検証している
- **部分重複**: セットアップや期待値の大半が共通
- **統合候補**: parameterized test や shared helper でまとめられる

#### C. unit 純度

- **pure unit**: 外部依存が隔離され、決定的
- **hidden integration**: unit を名乗るが外部依存や環境状態に触れている
- **integration 相当**: 実際には統合テストとして扱うべき

#### D. 外部依存

最低限、次を外部依存候補として扱う。

- HTTP / API / URL / RPC
- DB / queue / cache
- clock / timer / sleep / timeout / retry
- subprocess / shell / command
- filesystem
- environment variable / process-global state
- random / UUID / nondeterministic source

#### E. 安定性リスク

- flaky
- timing-sensitive
- order-dependent
- environment-dependent
- network-dependent

### 3. 問題の根拠を集める

発見ごとに、次のいずれかの根拠を必ず添える。

- 現行コードに対象機能が見当たらない
- docs / README / public API とズレている
- 同じ振る舞いを別テストがすでにカバーしている
- 単一の内部実装に過剰結合している
- テストが直接外部依存を叩いている
- sleep / now / random / env / shared state に依存している

根拠が弱い場合は断定せず、`要確認` に落とす。

### 4. 改善方針を出す

各発見に対して、次のどれが妥当かを選ぶ。

- 削除
- 統合
- parameterized test 化
- shared helper 抽出
- mock 化
- fake 化
- stub 化
- dependency injection 導入
- integration test へ移管
- contract test として明示的に残す

## 削除候補にしやすいケース

次の条件が複数当てはまるほど、削除候補として強い。

- 対象機能が production code から消えている
- 公開 API / CLI / route / export に存在しない
- docs や README に現行機能として現れない
- 旧エラーメッセージや旧内部関数名だけを固定している
- 別テストが同じ振る舞いをより高い粒度で守っている
- 長期放置された skip / todo / deprecated テストである

ただし、互換性維持のために残している可能性があるなら、その前提を明記して `要確認` にする。

## 重複判定の軸

重複は単なる行数の近さではなく、次の 4 軸で見る。

1. セットアップ
2. 入力
3. 期待値
4. 守ろうとしている振る舞い

4 軸のうち 3 つ以上が実質同じなら、重複候補として扱ってよい。

## モックの判断原則

### モック・フェイクを勧めるケース

- unit test がネットワークへ出る
- unit test が DB を直接叩く
- unit test が現在時刻や sleep に依存する
- unit test が subprocess を起動する
- unit test が process-global state に依存する

### モックしない方がよいケース

- adapter / repository / HTTP client の integration test
- migration test
- CLI の smoke test
- 契約検証が主目的の contract test

この場合は「unit test からは分離し、integration test として明示する」方向を優先する。

## 言語別の具体シグナル

SKILL.md は言語非依存で進める。具体的な探索シグナルやモック手法が必要なときは、該当言語の reference を読む。

- JavaScript / TypeScript: `unit-test-hygiene/references/javascript-typescript.md`
- Python: `unit-test-hygiene/references/python.md`
- Go: `unit-test-hygiene/references/go.md`
- Rust: `unit-test-hygiene/references/rust.md`
- 共通ヒューリスティクス: `unit-test-hygiene/references/heuristics.md`
- mock / stub / fake の使い分け: `unit-test-hygiene/references/mocking-playbook.md`

## 出力フォーマット

以下の構造を基本に、日本語で返す。

```md
## テスト棚卸しサマリ
- 総評: ...
- 不要テスト候補: ...
- 重複/冗長候補: ...
- 外部依存混入候補: ...
- flaky リスク候補: ...

## 発見事項

### 1) 不要・旧仕様テスト
- 対象: `path/to/test`
- 判定: 削除候補 / 要確認
- 根拠: ...
- 推奨アクション: ...

### 2) 重複・冗長テスト
- 対象: ...
- 重複内容: ...
- 推奨アクション: ...

### 3) 外部依存の直接利用
- 対象: ...
- 依存種別: API / URL / timer / command / DB / filesystem / env
- 問題: ...
- 推奨境界: mock / fake / DI / integrationへ移管

### 4) flaky / 不安定要因
- 対象: ...
- 不安定要因: ...
- 推奨アクション: ...

## 優先度付き整理計画
- P0: ...
- P1: ...
- P2: ...
- P3: ...

## モック/分離設計メモ
- どこを境界にするか
- どこは fake が良いか
- どこは integration test として残すべきか
```

## よい出力の条件

- ファイルやテスト名を具体的に挙げる
- 推測と事実を分ける
- 「削除」「統合」「モック」「移管」を混同しない
- 根拠なしで obsolete と断定しない
- すぐ直すべき順番がわかるように優先度をつける
- 実装者が次の作業を issue に切り出せる粒度にする

## 避けること

- テストは多いほど良い、という前提で話す
- すべての外部依存を機械的にモック対象にする
- integration test の価値を無視する
- 実装詳細 assertions の削減だけを目的化する
- 断片的な grep だけで大胆な削除提案をする
