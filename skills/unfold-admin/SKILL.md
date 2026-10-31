---
name: unfold-admin
description: Build and modify Django admin interfaces with Django Unfold (django-unfold), the Tailwind-based admin theme. Use when a project has "unfold" in INSTALLED_APPS or imports unfold.*, or when the user asks to style or extend Django admin with Unfold. Covers the UNFOLD settings dict, sidebar and tabs, ModelAdmin options, @display and @action decorators, custom actions and dialogs, list filters, inlines, widgets, dashboards and components, custom pages and sites, theming, and integrations such as import-export, simple-history, guardian, constance and celery-beat.
license: MIT
compatibility: Targets django-unfold 0.110.x (Python 3.12+, Django 5.2-6.1). Documentation snapshot from v0.105.0 (2026-09-05).
metadata:
  unfold-version: "0.110.0"
  docs-snapshot: "2026-09-05"
  skill-version: "1.0.0"
---

# Django Unfold

Unfold is a theme and extension layer for `django.contrib.admin`. It is **not** a separate admin. You keep Django's admin APIs and swap in Unfold base classes, decorators, widgets and settings.

## Version notice

- **Target:** django-unfold **0.110.0**, Python 3.12–3.15, Django 5.2, 6.0 and 6.1. Django 5.1 was dropped in 0.97.
- **Docs snapshot:** official docs as of v0.105.0 (2026-09-05). Later features (0.106–0.110) are marked "not in docs snapshot" in the references.
- **Check the installed version before relying on newer features:** `pip show django-unfold`.
- Unfold is pre-1.0, so minor releases can break things. Check the changelog when upgrading.

## Non-negotiable conventions

1. `"unfold"` goes **before** `"django.contrib.admin"` in `INSTALLED_APPS`. Contrib apps (`unfold.contrib.filters`, `.forms`, `.inlines`, and the integrations) go after `unfold`.
2. Every admin class inherits `unfold.admin.ModelAdmin`. Inlines use `unfold.admin.StackedInline` and `TabularInline`. Never use the Django base classes; they render unstyled and ignore Unfold options.
3. Re-register `User` and `Group` with Unfold forms (`unfold.forms.UserChangeForm`, `UserCreationForm`, `AdminPasswordChangeForm`).
4. Third-party admins (celery-beat, waffle, simple-history and others) must be unregistered and re-registered with `ModelAdmin` mixed in.
5. Use `unfold.decorators.action` and `unfold.decorators.display`, not Django's.
6. Plain forms on custom pages, actions and dialogs need **explicit** `unfold.widgets.*` widgets. ModelAdmin forms get them automatically.
7. Settings values for URLs and paths are callables (`lambda request: ...`) or `reverse_lazy`. Callbacks are dotted strings. Titles use `gettext_lazy`.
8. Custom sites subclass `unfold.sites.UnfoldAdminSite`, never `AdminSite`.
9. Icons are [Material Symbols](https://fonts.google.com/icons) names. Colour variants are `default`, `primary`, `success`, `info`, `warning` and `danger`.

## Common pitfalls

- **Adding Tailwind classes to your templates and expecting them to work.** They are not compiled. Use plain CSS or build Tailwind 4 and load it through `STYLES` → [styling.md](references/styling.md).
- **Setting `SIDEBAR.navigation` and forgetting models.** It replaces the automatic app list. Custom pages are never auto-linked.
- **Typos in dotted paths.** A dotted string that fails to import is used as a literal value, with no error. Sidebar items without a `link` are dropped silently.
- **Custom ModelAdmin URLs after `super().get_urls()`.** They never match. Prepend them.
- **Row-action permissions.** They get no `object_id`, so per-row permission checks are impossible.
- **Submit-line actions.** They run *after* save, so re-save any changes you make in the handler.
- **Dialog actions.** They need a `BaseDialogForm` subclass and must return an `HX-Redirect` header.
- **Input filters** (text, numeric, date, autocomplete) without `list_filter_submit = True`.
- **Sections or `show_count` on big tables** without `prefetch_related`, which causes N+1 queries.
- **Datasets** that do not scope their queryset to the parent object, or that use `list_filter`, which is unsupported.
- **Copying docs examples verbatim.** Several have syntax errors → [troubleshooting.md](references/troubleshooting.md#known-errors-in-official-docs-examples).
- **Using removed APIs:** `hide_title` (now `show_title`), `unfold.contrib.import_export.admin`, and modeltranslation support.

## Decision guide

| The user wants… | Use | Reference |
|---|---|---|
| Install or brand the admin, set up login or the environment badge | `UNFOLD` settings | [configuration.md](references/configuration.md) |
| Re-style User and Group, avatar, languages | auth forms, user properties, `SHOW_LANGUAGES` | [configuration.md](references/configuration.md) |
| Sidebar links, badges, permissions | `UNFOLD["SIDEBAR"]` | [navigation.md](references/navigation.md) |
| Tabs above changelist or changeform pages | `UNFOLD["TABS"]` | [navigation.md](references/navigation.md) |
| Tabs inside the form | fieldset `"classes": ["tab"]`, inline `tab = True` | [model-admin.md](references/model-admin.md), [inlines.md](references/inlines.md) |
| Cmd+K search, site header dropdown | `COMMAND`, `SITE_DROPDOWN` | [navigation.md](references/navigation.md) |
| Coloured status badges, two-line cells, dropdown cells, prices | `@display(label=…, header=…, dropdown=…, formatting="price")` | [model-admin.md](references/model-admin.md) |
| Show or hide fields based on other fields | `conditional_fields` | [model-admin.md](references/model-admin.md) |
| Expandable rows with related data | `list_sections` | [model-admin.md](references/model-admin.md) |
| Related changelist inside an edit page | `change_form_datasets` | [model-admin.md](references/model-admin.md) |
| Drag-and-drop ordering | `ordering_field` (changelist or inline) | [model-admin.md](references/model-admin.md), [inlines.md](references/inlines.md) |
| Huge tables, slow `COUNT` | `InfinitePaginator` | [model-admin.md](references/model-admin.md) |
| Buttons on changelist, row, detail or submit line | `actions_list` / `_row` / `_detail` / `_submit_line` | [actions.md](references/actions.md) |
| Confirm or collect input before an action | `@action(dialog={...})` | [actions.md](references/actions.md) |
| Better filters (text, range, date, checkbox, autocomplete) | `unfold.contrib.filters.admin` | [filters.md](references/filters.md) |
| Inline pagination, collapsing, counts, nesting, non-FK inlines | inline attributes | [inlines.md](references/inlines.md) |
| Rich text, arrays, autocomplete fields, crispy forms, JSON schema | `unfold.contrib.forms`, `unfold.fields` | [forms-and-widgets.md](references/forms-and-widgets.md) |
| Dashboard with KPIs, charts, tables | `admin/index.html`, `DASHBOARD_CALLBACK`, `{% component %}` | [dashboards.md](references/dashboards.md) |
| A standalone page in the admin chrome | `UnfoldModelAdminViewMixin` | [custom-pages-and-sites.md](references/custom-pages-and-sites.md) |
| A second admin site, or replacing `admin.site` | `UnfoldAdminSite`, `BasicAppConfig` | [custom-pages-and-sites.md](references/custom-pages-and-sites.md) |
| Colours, dark mode, radius, custom CSS or JS | `COLORS`, `THEME`, `STYLES` | [styling.md](references/styling.md) |
| import-export, simple-history, guardian, constance, celery-beat, waffle, hijack, money, location-field, reversion | per-package recipe | [integrations.md](references/integrations.md) |
| Something renders wrong or errors | symptom table | [troubleshooting.md](references/troubleshooting.md) |

## Reference index

Load **only** the file the task needs. Each one is self-contained and links to the official pages.

| File | Contents |
|---|---|
| [configuration.md](references/configuration.md) | Install, `INSTALLED_APPS`, every top-level `UNFOLD` key, login, environment, auth admin, avatar, i18n |
| [navigation.md](references/navigation.md) | `SIDEBAR`, `TABS` (static, dynamic, `tab_list`), `SITE_DROPDOWN`, `COMMAND` |
| [model-admin.md](references/model-admin.md) | ModelAdmin option table, `@display`, conditional fields, fieldset tabs, sections, datasets, paginator, sortable changelist, readonly JSON |
| [actions.md](references/actions.md) | Action types, `@action` params, permissions, dropdowns, dialogs, form-page actions |
| [filters.md](references/filters.md) | Filter class chooser, custom filter bases, layout options |
| [inlines.md](references/inlines.md) | Inline classes and options, sortable, paginated, nested, nonrelated |
| [forms-and-widgets.md](references/forms-and-widgets.md) | Widget catalogue, Array and Wysiwyg widgets, autocomplete fields, crispy forms, JSONSchemaField |
| [dashboards.md](references/dashboards.md) | Dashboard template, callback, component templates and params, component classes, data shapes |
| [custom-pages-and-sites.md](references/custom-pages-and-sites.md) | Custom views, `custom_urls`, `SITE_VIEWS`, `UnfoldAdminSite`, `BasicAppConfig` |
| [styling.md](references/styling.md) | `COLORS`, `THEME`, `BORDER_RADIUS`, `STYLES`/`SCRIPTS`, Tailwind 4, contributor build |
| [integrations.md](references/integrations.md) | Per-package setup and deprecations |
| [troubleshooting.md](references/troubleshooting.md) | Symptom → fix table, known docs errata |

## Workflow

1. **Inspect.**
   - Check the installed version (`pip show django-unfold`, or the lock file).
   - Check `INSTALLED_APPS` order and the existing `UNFOLD` dict.
   - Find which admin classes still inherit Django bases.
2. **Choose a feature** from the decision guide, then open its reference file. Prefer documented APIs. Mention it when you use something marked "not in docs snapshot".
3. **Implement.**
   - Add the required contrib app.
   - Inherit the Unfold classes.
   - Use lazy URLs and translations in settings.
   - Keep business logic out of templates. Prepare data in callbacks or component classes.
4. **Verify.**
   - Run `python manage.py check`.
   - Import-check the dotted callback paths: `python -c "from django.utils.module_loading import import_string; ..."` after `django.setup()`.
   - Run `python manage.py makemigrations --check` if you touched models, for example an ordering field.
   - Open the changelist and changeform in the browser if possible. Check the sidebar, dark mode, permissions as a non-superuser, and the query count on list pages.
   - For CSS changes, run `collectstatic` and confirm the file loads.
5. **Report** any undocumented or version-dependent behaviour you relied on.

Official docs: https://unfoldadmin.com/docs/ · Demo: https://demo.unfoldadmin.com · Source and changelog: https://github.com/unfoldadmin/django-unfold
