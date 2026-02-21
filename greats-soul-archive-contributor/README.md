# greats-soul-archive-contributor

A contributor workflow skill for **tumf/greats-soul-archive**.

This skill helps an agent (or a human with agent assistance) scaffold new profiles:

- Real people → `people/<slug>/`
- Fiction (public domain) → `fiction/public-domain/<slug>/`
- Fiction (inspired-by) → `fiction/inspired/<slug>/`

It generates:
- `IDENTITY.md`
- `SOUL.md`
- `sources.md`
- `meta.yml` (category/genre/tags)

## Quickstart

1) Clone the archive repo:

```bash
git clone https://github.com/tumf/greats-soul-archive
```

2) Scaffold a profile:

```bash
python3 scripts/scaffold_profile.py \
  --repo ./greats-soul-archive \
  --kind people \
  --slug grace-hopper \
  --name "Grace Hopper" \
  --category computing \
  --tags assistant
```

3) In the archive repo, rebuild the README index:

```bash
cd greats-soul-archive
python3 scripts/build_index.py
```

4) Open a PR.

## Notes

- Keep facts in `sources.md`; keep persona in `SOUL.md`.
- For modern fiction: avoid verbatim dialogue/catchphrases and long quotes.
