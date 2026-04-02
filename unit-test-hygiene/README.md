# unit-test-hygiene

既存のユニットテスト群を整理するためのスキルです。不要なテスト、重複・冗長なテスト、外部依存を直接叩いている“unit test らしくないテスト”を見つけ、削除・統合・モック化・integration test への移管方針まで整理します。

## できること

- 古い仕様や廃止機能に紐づくテストの発見
- 重複・冗長テストの整理
- API / URL / timer / command / DB / filesystem / env 依存の検出
- flaky テストの予兆検出
- mock / stub / fake / DI 境界の提案
- unit test / integration test の責務分離

## 向いている依頼

- 「古いテストを掃除したい」
- 「重複テストを減らしたい」
- 「API や DB を直で叩いている unit test を見つけたい」
- 「モック化の境界を整理したい」
- 「テストが遅い・不安定」
- 「unit と integration の境界が曖昧」

## 出力イメージ

- テスト棚卸しサマリ
- 不要/要確認テスト一覧
- 重複/冗長テスト一覧
- 外部依存の直接利用一覧
- 優先度付き整理計画
- モック/分離設計メモ

## 付属 references

- `references/heuristics.md`
- `references/mocking-playbook.md`
- `references/javascript-typescript.md`
- `references/python.md`
- `references/go.md`
- `references/rust.md`

## インストール

```bash
npx skills add tumf/skills --skill unit-test-hygiene
```

## 例

- 「この repo の unit test を整理して。古い機能向けのテスト、重複、API 直叩きを洗い出して」
- 「pytest のテスト群を棚卸しして、DB 直結や time.sleep 依存を mock/fake に寄せる計画を出して」
- 「Jest テストが遅くて flaky。unit と integration を分離する観点で見て」
