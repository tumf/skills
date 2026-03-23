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

- "Adopt OpenSpec mid-project and derive a baseline spec from the current implementation."
- "Use the brownfield workflow to create `openspec/specs/` from an existing repo."
- "I want to introduce OpenSpec to this brownfield project."
- "Create the current source of truth for OpenSpec from the existing implementation."
- "Start with baseline specs for auth and billing only."

## Notes

- Reverse-engineered specs are drafts until reviewed by a human.
- Specs should capture observable behavior and constraints, not internal implementation trivia.
- Start with high-change or high-risk domains first instead of trying to spec the whole repo in one pass.
