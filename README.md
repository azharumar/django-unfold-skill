# django-unfold-skill

An [Agent Skill](https://agentskills.io/specification) that teaches AI coding agents how to build and change Django admin interfaces with [Django Unfold](https://unfoldadmin.com/docs/).

> **Version notice:** targets **django-unfold 0.110.0** (Python 3.12–3.15, Django 5.2 / 6.0 / 6.1). The knowledge comes from the official documentation as of **v0.105.0 (2026-09-05)** and was checked against the 0.110.0 source. Features added after the docs snapshot are labelled in the references. See [docs/coverage.md](docs/coverage.md).

## Why an agent needs it

Unfold looks like ordinary Django admin, but it has its own rules that agents often get wrong:
- App ordering.
- Unfold base classes everywhere, including third-party admins.
- Lazy callables in settings.
- Uncompiled Tailwind classes.
- Separate signatures for each action type.
- Dialog actions that return `HX-Redirect`.
- Several examples in the official docs that do not run as written.

The skill packs these rules, plus a feature-selection guide, into a small entry file. Detailed references load only when a task needs them.

## What it covers

- Installation and every `UNFOLD` setting.
- Sidebar, tabs, site dropdown and command palette.
- `ModelAdmin` options and `@display`.
- Conditional fields, sections, datasets, the infinite paginator and sortable changelists.
- All action types and dialogs.
- Every contrib filter.
- Inlines: sortable, paginated, nested and nonrelated.
- Widgets, autocomplete fields, crispy forms and `JSONSchemaField`.
- Dashboards and components.
- Custom pages and sites.
- Theming and Tailwind.
- Integrations: import-export, simple-history, guardian, constance, celery-beat, waffle, hijack, money, location-field, json-widget, djangoql and reversion.
- A troubleshooting table.

## Layout

```
django-unfold-skill/
├── skills/unfold-admin/          # the skill; copy this directory
│   ├── SKILL.md                  # entry point: conventions, pitfalls, decision guide, workflow
│   └── references/               # loaded on demand, one topic per file
│       ├── configuration.md      ├── forms-and-widgets.md
│       ├── navigation.md         ├── dashboards.md
│       ├── model-admin.md        ├── custom-pages-and-sites.md
│       ├── actions.md            ├── styling.md
│       ├── filters.md            ├── integrations.md
│       ├── inlines.md            └── troubleshooting.md
├── docs/coverage.md              # page-by-page documentation coverage map
├── scripts/validate.py           # frontmatter, link and coverage checks
├── CHANGELOG.md  CONTRIBUTING.md  LICENSE
```

## Installation

The skill is the `skills/unfold-admin/` directory. The Agent Skills specification defines what goes inside a skill, not where agents look for one, so check your agent's documentation. Common locations:

| Scope | Path |
|---|---|
| Project, cross-client convention | `<project>/.agents/skills/unfold-admin/` |
| User, cross-client convention | `~/.agents/skills/unfold-admin/` |
| Claude Code | `<project>/.claude/skills/unfold-admin/` or `~/.claude/skills/unfold-admin/` |

```bash
git clone https://github.com/azharumar/django-unfold-skill.git
```

```bash
mkdir -p .agents/skills && cp -r django-unfold-skill/skills/unfold-admin .agents/skills/
```

Agents that support the format load the `name` and `description` at start-up. They read `SKILL.md` when a task mentions Unfold or Django admin styling, and open a reference file only when the task needs it. With agents that do not support skills, point the agent at `skills/unfold-admin/SKILL.md` by hand.

## Usage

Ask normally. For example:
- "Add a status badge column and a date-range filter to the Order admin."
- "Put our reports page in the sidebar."
- "Make the celery-beat admin match Unfold."

A sidebar change loads only `SKILL.md` and `navigation.md`.

## Token budget

- `SKILL.md` is 117 lines, about 2,600 tokens. That is under the spec's 5,000-token guidance.
- Each reference file is about 850–2,250 tokens.
- A typical task loads `SKILL.md` and one reference, about 4,000 tokens. The raw docs snapshot is about 50,000 tokens.
- Run `python scripts/validate.py` for current figures.

## Documentation coverage

- All 76 content pages of the docs snapshot were reviewed and mapped to a reference file. The other 12 files in the docs tree are section index stubs with no content.
- Two pages that exist only on the live site (django-reversion and django-reversion-compare) could not be read. They are recorded as unresolved.
- Details, post-snapshot features and update steps are in [docs/coverage.md](docs/coverage.md).

## Compatibility

| Item | Value |
|---|---|
| Unfold (code verified) | 0.110.0 |
| Docs snapshot | v0.105.0 + 3 commits (2026-09-05) |
| Python | 3.12–3.15 (`requires-python >=3.12`) |
| Django | 5.2, 6.0, 6.1 (classifiers); 5.1 dropped in 0.97 |
| Optional extras | `django-unfold[pygments]` (readonly JSON highlighting), `django-unfold[jsonschema]` (`JSONSchemaField` validation) |
| Breaking or removal notes | `hide_title`→`show_title` (0.104); modeltranslation deprecated (0.102) and removed; `unfold.contrib.import_export.admin` removed |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: cite an official page or a release's source for every change, keep `SKILL.md` small, update `docs/coverage.md`, and run `python scripts/validate.py`.

## Licence and attribution

- The skill content is released under the [MIT License](LICENSE).
- Django Unfold is © Unfold Admin, also MIT licensed. This project is not affiliated with Unfold Admin.
- The reference files summarise and paraphrase the official documentation and link to each source page. Code snippets are adapted from the documentation's examples, with errors corrected.
