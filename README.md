# Skills

A collection of skills for AI coding agents.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Installation

```bash
npx skills add tumf/skills

# Install only one skill
npx skills add tumf/skills --skill jp-grants
```

## Available Skills

<!-- skills:start -->

### agentic-cli-design

Design principles for building CLI tools that LLM/AI agents can safely and reliably operate. Provides 7 core principles (Machine-readable, Non-interactive, Idempotent, Safe-by-default, Observable, Context-efficient, Introspectable) with scorecard, templates, and anti-patterns.

[Documentation](./agentic-cli-design/README.md)

### ai-chat-frontend

アプリ組み込み AI チャットフロントエンドの設計・実装ガイド。 前半は言語非依存の抽象設計パターン（ストリーミングファースト、チャット状態マシン、 メッセージモデル、楽観的UI、エラーリカバリ、UX原則、マルチセッション、サーバー設計原則）、 後半は Vercel AI SDK (useChat) による TypeScript 具体実装。 フレームワーク非依存（Next.js, React SPA, Vue, Svelte, SvelteKit, Nuxt 対応）。.

[Documentation](./ai-chat-frontend/README.md)

### autoresearch-agent

Delegate autoresearch tasks to a headless Claude Code sub-agent process.

[Documentation](./autoresearch-agent/README.md)

### brainstorm-frameworks

Use this skill whenever the user asks for brainstorming, ideation, concept expansion, service improvement ideas, strategy options, workshop structure, or says thinking is stuck and needs more perspectives. Select and apply one or more brainstorming frameworks based on the user's goal, solo vs group setting, divergence vs convergence need, and business vs creative context. Use it even if the user does not name a framework.

[Documentation](./brainstorm-frameworks/README.md)

### business-planning

Use this skill whenever the user asks to create, structure, review, or refine a business plan, new business proposal, growth strategy, GTM outline, or venture hypothesis. Build a rational, persuasive business plan with reader-specific framing and bottom-up numerical planning. Distinguish researched facts from benchmarks and estimates, use frameworks only as supporting tools, and forecast outcomes from causal drivers instead of reverse-engineering a desired result. Use it even when the user only says "事業計画", "戦略を考えたい", "新規事業を整理したい", or asks for AI agent / SaaS business planning without naming any framework.

[Documentation](./business-planning/README.md)

### clawdbot-config

Comprehensive Clawdbot configuration and skills system management.

[Documentation](./clawdbot-config/README.md)

### dashboard-design-guidebook

デジタル庁のダッシュボードデザイン実践ガイドブックに基づく、見やすいダッシュボード設計・作成のガイド。グラフ選び、レイアウト、カラーパレット、アクセシビリティ、チェックリストを網羅。.

[Documentation](./dashboard-design-guidebook/README.md)

### fermi-estimation

Solve user questions with defensible Fermi estimates using explicit assumptions, source-backed inputs, uncertainty ranges, and sensitivity analysis.

[Documentation](./fermi-estimation/README.md)

### firecrawl

Comprehensive web scraping, crawling, and data extraction toolkit powered by Firecrawl API. Provides scripts for single-page scraping (scrape.py), web search (search.py), URL discovery (map.py), multi-page crawling (crawl.py), structured data extraction (extract.py), and autonomous data gathering (agent.py).

[Documentation](./firecrawl/README.md)

### gogcli

Fast, script-friendly CLI for Google services via `gog`. Use this skill whenever the user needs to work with Gmail, Google Calendar, Drive, Docs, Sheets, Slides, Forms, Apps Script, Contacts, Tasks, People, Chat, Classroom, Groups, Admin, or Keep from the terminal, especially for Google Workspace automation, account setup, OAuth/client configuration, service accounts, domain-wide delegation, or JSON/scriptable workflows. Prefer this skill even when the user does not mention `gog` explicitly but is clearly trying to automate or inspect Google services from a CLI or agent workflow.

[Documentation](./gogcli/README.md)

### greats-soul-archive-contributor

Contribute new profiles to tumf/greats-soul-archive.

[Documentation](./greats-soul-archive-contributor/README.md)

### jp-grants

Collect and answer questions about Japanese subsidies/grants (補助金・助成金) with up-to-date sources.

[Documentation](./jp-grants/README.md)

### openclaw-agent-creator

Create and maintain OpenClaw agent workspaces using the "Memory as Documentation" layout.

[Documentation](./openclaw-agent-creator/README.md)

### opencode-agent-creator

Create specialized OpenCode agents with proper configuration for primary agents and subagents.

[Documentation](./opencode-agent-creator/README.md)

### opencode-command-creator

Create custom OpenCode commands with proper structure, trigger descriptions, arguments, and configuration.

[Documentation](./opencode-command-creator/README.md)

### openspec-brownfield-baseline

Introduce OpenSpec into an existing codebase by deriving baseline specs from current behavior, then switch future work to change-driven development.

[Documentation](./openspec-brownfield-baseline/README.md)

### oss-publish

Open source publication and release hygiene for repositories and CLIs (language-agnostic): choose and add LICENSE, prepare README/CONTRIBUTING/SECURITY/CODE_OF_CONDUCT, standardize versioning/tags/releases and release notes, set up CI matrices, quality gates (pre-commit/pre-push), and safe-by-default automation/bootstrapping.

[Documentation](./oss-publish/README.md)

### product-improvement-proposal

Propose concrete, high-leverage product/UX improvements to increase a software project's appeal and retention.

[Documentation](./product-improvement-proposal/README.md)

### python-uv-project

Scaffold opinionated Python projects with uv as the package/project manager and `uv init` as the bootstrap step.

[Documentation](./python-uv-project/README.md)

### rust-cli

Design and implementation guidance for maintainable Rust CLIs with strong ergonomics, machine-friendly behavior, testable structure, and release automation.

[Documentation](./rust-cli/README.md)

### slack-rs

Slack Web API automation via the slack-rs CLI (Rust).

[Documentation](./slack-rs/README.md)

### unit-test-hygiene

Audit and reorganize an existing test suite to remove outdated tests, reduce duplication, and isolate external dependencies from unit tests. Use this skill whenever the user wants to clean up tests, find obsolete or redundant tests, detect unit tests that directly hit APIs/URLs/timers/commands/databases/filesystems/env state, improve mock boundaries, reduce flakiness, or clarify the boundary between unit and integration tests. Use it even if the user only says things like "整理したい", "モック化したい", "テストが遅い", or "古いテストを掃除したい".

[Documentation](./unit-test-hygiene/README.md)

### wt-setup

Create and maintain `.wt/setup` bootstrap scripts for git worktree environments. The `.wt/setup` script is a repository-local convention executed automatically by supporting tools (e.g. wt) when creating new git worktrees.

[Documentation](./wt-setup/README.md)

### youtube-summarizer

Summarize YouTube videos by extracting and analyzing auto-generated subtitles.

[Documentation](./youtube-summarizer/README.md)

<!-- skills:end -->

---

*More skills coming soon...*

## Usage

Skills are available once installed. Use the skill name in your request.

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `README.md` - Full documentation
- `scripts/` - Executable scripts (optional)
- `references/` - Supporting documentation (optional)

## License

MIT
