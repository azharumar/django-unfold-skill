# Contributing

## Principles

1. **Official sources only.** Each fact must come from either an unfoldadmin.com docs page or the source code of a tagged django-unfold release.
   - Label anything that comes from source alone as "not in docs snapshot".
   - Never add speculative APIs.
2. **Progressive disclosure.**
   - `SKILL.md` holds conventions, pitfalls and routing only.
   - Details go in one reference file.
   - Do not repeat an example across files; link to it.
3. **Token economy.**
   - Prefer tables and minimal code.
   - Skip generic Django knowledge.
   - Keep `SKILL.md` under about 250 lines and each reference under about 2,000 tokens.
4. **Do not copy known-broken docs examples.** Fix them, and add the error to the errata table in `troubleshooting.md`.
5. **British English** in prose.

## Updating for a new Unfold release

1. Read the django-unfold `CHANGELOG.md` entries since the version in `SKILL.md` metadata.
2. Compare the live docs navigation with `docs/coverage.md`, then add or update rows and reference sections.
3. Re-check imports and setting keys against the new source, for example `src/unfold/settings.py` (`CONFIG_DEFAULTS`) and `admin.py`.
4. Bump the versions in `SKILL.md` (`compatibility` and `metadata`), the README version notice and table, and `CHANGELOG.md`.
5. Run the checks:

```bash
python scripts/validate.py
```

```bash
pip install skills-ref && skills-ref validate skills/unfold-admin
```

## Pull requests

- Describe which official page or release each change comes from.
- One topic per PR where practical.
