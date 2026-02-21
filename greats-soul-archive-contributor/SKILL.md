---
name: greats-soul-archive-contributor
description: "Contribute new profiles to tumf/greats-soul-archive. Use when user says they want to add/post/submit a new person/character profile, open a PR, scaffold IDENTITY.md/SOUL.md/sources.md, add meta.yml (category/tags), run scripts/build_index.py, or follow the repo contribution rules."
---

# Greats Soul Archive Contributor

## Repo

- GitHub: https://github.com/tumf/greats-soul-archive

## What to do (happy path)

1. Pick a destination:
   - Real person → `people/<slug>/`
   - Fiction public domain → `fiction/public-domain/<slug>/`
   - Fiction inspired-by → `fiction/inspired/<slug>/`

2. Scaffold the folder + files using the script:

```bash
python3 scripts/scaffold_profile.py \
  --repo ~/tmp/greats-soul-archive \
  --kind people \
  --slug grace-hopper \
  --name "Grace Hopper" \
  --category computing \
  --tags assistant
```

Kinds:
- `people`
- `fiction-public-domain`
- `fiction-inspired`

3. Edit the generated files:
   - `IDENTITY.md` should be short.
   - `SOUL.md` should be actionable (principles, comms style, failure modes).
   - `sources.md` must be real references; keep uncertainty explicit.

4. Update the README index:

```bash
cd <repo>
python3 scripts/build_index.py
```

5. Ensure meta is valid:
   - People meta: `people/_meta.schema.md`
   - Fiction meta: `fiction/_meta.schema.md`

6. Open a PR.

## Safety / quality rules (must follow)

- Don’t present speculation as fact.
- Avoid defamation/harassment.
- Living people: be extra conservative; prefer direct sources.
- Fiction inspired-by: do not paste long quotes; do not try to reproduce verbatim dialogue/catchphrases.

## When you need to look things up

- Repo rules: `CONTRIBUTING.md`
- Fiction rules: `fiction/_guide.md`
