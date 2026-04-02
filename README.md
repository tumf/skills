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

### autoresearch-agent

Delegate autoresearch tasks to a headless Claude Code sub-agent process.

[Documentation](./autoresearch-agent/README.md)

### clawdbot-config

Comprehensive Clawdbot configuration and skills system management.

[Documentation](./clawdbot-config/README.md)

### fermi-estimation

Solve user questions with defensible Fermi estimates using explicit assumptions, source-backed inputs, uncertainty ranges, and sensitivity analysis.

[Documentation](./fermi-estimation/README.md)

### firecrawl

Comprehensive web scraping, crawling, and data extraction toolkit powered by Firecrawl API. Provides scripts for single-page scraping (scrape.py), web search (search.py), URL discovery (map.py), multi-page crawling (crawl.py), structured data extraction (extract.py), and autonomous data gathering (agent.py).

[Documentation](./firecrawl/README.md)

### gogcli

Fast, script-friendly CLI for Google Workspace and Gmail.

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

Audit and reorganize an existing test suite to remove outdated tests, reduce duplication, and isolate external dependencies from unit tests.

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
