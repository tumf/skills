# OSS publication checklist

Use this as a practical preflight checklist before making a repository public or cutting a first release.

## Make repo public (preflight)

- License selected and added (`LICENSE`)
- Ownership clarified (copyright holder, org)
- README present (what it is, who it's for, quick start)
- Contribution path defined (`CONTRIBUTING.md`)
- Code of conduct added (`CODE_OF_CONDUCT.md`)
- Security reporting defined (`SECURITY.md`)
- Secrets scan: no API keys/tokens committed; `.env` and credentials files are gitignored
- CI runs on default branch
- Release/versioning strategy decided (SemVer or ecosystem-specific)

## Cut a release (preflight)

- Working tree clean; all changes committed
- Tests pass (full suite)
- Lint/format checks pass
- Version bumped (single source of truth)
- Tag created on release commit
- Release notes drafted (what changed + upgrade notes)
- Artifacts built from the release commit (if distributing binaries)
- Verification notes documented (checksums, provenance, SBOM if used)
