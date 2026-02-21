# README.md guide (OSS)

Goal: a reader should understand the project in **3 seconds**, run it in **1 minute**, and see value in **10 minutes**.

## Principles

- **Be concrete early**: avoid abstract mission statements.
- **Optimize for copy/paste**: commands should work as written.
- **Show, then tell**: a short demo beats paragraphs.
- **Keep it current**: remove sections you do not maintain.
- **Make releases predictable**: document versioning and how releases are managed (at a high level).

## Recommended structure

1) **What / Why** (overview + differentiator)
2) **Demo** (CLI output or screenshots)
3) **Features** (short bullets)
4) **Installation** (clear per-package-manager sections)
5) **Quick Start** (shortest path to success)
6) **Usage** (common recipes + options table)
7) **Configuration** (example config + defaults)
8) **Architecture** (only if it adds real value; link to deeper docs)
9) **Development** (only essential commands; link to `CONTRIBUTING.md`)
10) **Versioning & Releases** (how version numbers work + why automated management matters)
11) **Roadmap** (optional, but must be honest)
12) **License**

## Versioning & release management (high level)

Even if your project is small, version numbers and predictable releases reduce friction for users, packagers, and automation.

- **Version numbers**: state the policy (e.g. SemVer) and where the version is defined.
- **Change communication**: explain how users learn what changed (release notes / changelog).
- **Automation is necessary**: releases should be repeatable and low-risk; prefer an automated workflow that can:
  - bump version in the single source of truth
  - create a tag/release
  - produce release notes
  - attach artifacts (if any)

Keep this section tool-agnostic; implementation differs by language/ecosystem.

## Badges (optional)

Place at the top, but keep it minimal.

```markdown
![CI](https://github.com/<org>/<repo>/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)
```

## Copy/paste template (CLI/tool)

Replace `<...>` placeholders.

```markdown
# <ProjectName>

<One-line tagline: what it does for whom.>

## Overview

<ProjectName> is a <tool/service/library> that <does X>.
It is designed for <target users> who need <core value>.

### Why

- <Problem this solves>
- <Another problem>
- <Differentiator / unique approach>

## Demo

```bash
$ <project> --help
$ <project> <example-command>
<example output>
```

<!-- If you have a UI, include screenshots under ./assets/ and reference them here. -->

## Features

- <Fast / lightweight / safe-by-default>
- <Cross-platform / single binary / etc>
- <Automation-friendly output modes if applicable>

## Installation

### <Package manager>

```bash
<install command>
```

### From source

```bash
git clone https://github.com/<org>/<repo>
cd <repo>
<build or install command>
```

## Quick Start

```bash
<project> init
<project> run
```

## Usage

Common examples:

```bash
<project> run --config config.toml
<project> status --json
```

### Options

| Flag | Description |
|---|---|
| `--config <path>` | Path to config file |
| `--verbose` | Enable debug logs |

## Configuration

Example:

```toml
<example config>
```

## Development

```bash
<test command>
<lint command>
```

See `CONTRIBUTING.md` for full contributor workflow.

## Roadmap

- [x] v0.1 <milestone>
- [ ] v0.2 <milestone>

## License

<License name>. See `LICENSE`.
```

## Copy/paste section: Versioning & Releases

Add this section if the project will be consumed by others.

```markdown
## Versioning & Releases

This project follows <SemVer|other>.

- Version source of truth: <where the version lives>
- Release notes: <where users find changes>

Releases should be reproducible and low-risk. We use an automated release workflow to manage version bumps, tags, and release notes.
```

## Common anti-patterns

- Overview is vague (reader cannot tell what the project actually does).
- No Quick Start.
- Installation is ambiguous or mixes multiple methods without separation.
- Usage is either missing examples or is a long, unstructured dump.
- Versioning/release process is unclear (users cannot tell what changed or how to upgrade).
- README promises features that are not implemented or maintained.

## Good references (to learn from)

Look for repos where you can answer these quickly:

- What is it?
- How do I install it?
- What is the simplest working example?
