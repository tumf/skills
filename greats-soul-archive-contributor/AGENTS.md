# AGENTS.md — greats-soul-archive-contributor

This skill helps contributors add new profiles to:
- https://github.com/tumf/greats-soul-archive

## Default workflow

1. Ensure you have a local clone of the repo.
2. Run `scripts/scaffold_profile.py` to create a new profile folder.
3. Edit `IDENTITY.md` / `SOUL.md` / `sources.md` and fill real sources.
4. Run `python3 scripts/build_index.py` in the repo root.
5. Open a PR.

## Rules

- Keep facts in `sources.md`; keep persona/interpretation in `SOUL.md`.
- Be conservative for living people.
- For modern fiction (inspired-by), avoid verbatim dialogue/catchphrases and long quotes.
