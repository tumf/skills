# OpenSpec Brownfield Baseline

Introduce OpenSpec into an existing codebase by deriving baseline specs from current behavior, then switch future work to change-driven development.

This skill is for brownfield adoption: create a trustworthy baseline in `openspec/specs/` from the current implementation, then move future work into `openspec/changes/`.

## What You Get

- a proposed domain map for `openspec/specs/`
- guidance on choosing behavior-based boundaries instead of folder-based ones
- extraction of observable contracts from code, tests, APIs, and docs
- draft `spec.md` files with requirements and scenarios
- a review pass that separates intended behavior from inferred behavior and likely bugs
- a phased rollout approach for introducing OpenSpec without freezing delivery

## Example Prompts

- "OpenSpec を途中導入したい。今の実装から baseline spec を起こして"
- "既存 repo から `openspec/specs/` を作る手順を使って"
- "このプロジェクトを brownfield で OpenSpec 化したい"
- "現実装から OpenSpec の source of truth を作りたい"
- "まず auth と billing だけ baseline spec にして"

## Notes

- Reverse-engineered specs are drafts until reviewed by a human.
- Specs should capture observable behavior and constraints, not internal implementation trivia.
- Start with high-change or high-risk domains first instead of trying to spec the whole repo in one pass.
