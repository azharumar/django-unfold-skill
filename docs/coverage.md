# Documentation coverage map

What this file records: every page of the official Django Unfold documentation, whether it was reviewed, and where its knowledge lives in the skill. Use it to find gaps when the docs change.

## Source and method

- **Primary source:** the official docs are Markdown files that lived under `docs/` in [unfoldadmin/django-unfold](https://github.com/unfoldadmin/django-unfold). They were removed from that repository in commit `7d031442` (2026-09-05, "chore: cleanup docs"). This skill uses the tree at its parent, `807f4ce1`, three commits after the **v0.105.0** tag. That is the newest docs source that is publicly versioned.
- **Live site:** `https://unfoldadmin.com/docs/` was **not reachable** from the build environment, because of a network policy. URLs below are derived from the source paths, using the same scheme as the URLs in the Unfold README. They were not fetched.
- **Code verification:** imports, class names, settings keys and attributes used in the skill were checked against the **v0.110.0** source (2026-10-13). Differences are noted in the references.
- **Status values:**
  - `reviewed`: read in full and incorporated.
  - `n/a`: a section index page with front matter only.
  - `inaccessible`: known to exist but could not be read.

## Statistics

| Metric | Count |
|---|---|
| Source files in the docs tree | 88 |
| Section index stubs (no body) | 12 |
| Content pages | 76 |
| Content pages reviewed and mapped | 76 (100%) |
| Live-only pages known but inaccessible | 2 |
| Pages documenting removed or deprecated features | 1 (django-modeltranslation) |
| Docs code examples with errors (corrected in skill) | 16, see `troubleshooting.md` |

## Page inventory

Reference paths are relative to `skills/unfold-admin/references/`.


### actions

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Action with form example](https://unfoldadmin.com/docs/actions/action-form-example/) | `actions/action-form-example.md` | intermediate form page | reviewed | actions.md |
| [Changeform actions](https://unfoldadmin.com/docs/actions/changeform/) | `actions/changeform.md` | actions_detail | reviewed | actions.md |
| [Changeform submitline actions](https://unfoldadmin.com/docs/actions/changeform-submitline/) | `actions/changeform-submitline.md` | actions_submit_line | reviewed | actions.md |
| [Changelist actions](https://unfoldadmin.com/docs/actions/changelist/) | `actions/changelist.md` | actions_list | reviewed | actions.md |
| [Changelist row actions](https://unfoldadmin.com/docs/actions/changelist-row/) | `actions/changelist-row.md` | actions_row, permission limitation | reviewed | actions.md |
| [Actions with dialog](https://unfoldadmin.com/docs/actions/dialog-actions/) | `actions/dialog-actions.md` | dialog, BaseDialogForm, before/after templates | reviewed | actions.md |
| [Dropdown action](https://unfoldadmin.com/docs/actions/dropdown-actions/) | `actions/dropdown-actions.md` | dropdown groups | reviewed | actions.md |
| [Actions](https://unfoldadmin.com/docs/actions/) | `actions/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [Introduction to actions](https://unfoldadmin.com/docs/actions/introduction/) | `actions/introduction.md` | types, permissions, icon, variant, hide defaults | reviewed | actions.md |

### components

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Component - Button](https://unfoldadmin.com/docs/components/button/) | `components/button.md` | button params | reviewed | dashboards.md |
| [Component - Card](https://unfoldadmin.com/docs/components/card/) | `components/card.md` | card params | reviewed | dashboards.md |
| [Component - Chart](https://unfoldadmin.com/docs/components/chart/) | `components/chart.md` | bar/line charts, dataset options | reviewed | dashboards.md |
| [Component - Cohort](https://unfoldadmin.com/docs/components/cohort/) | `components/cohort.md` | cohort data shape | reviewed | dashboards.md |
| [Component class](https://unfoldadmin.com/docs/components/component-class/) | `components/component-class.md` | BaseComponent, register_component | reviewed | dashboards.md |
| [Components](https://unfoldadmin.com/docs/components/) | `components/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [Introduction to components](https://unfoldadmin.com/docs/components/introduction/) | `components/introduction.md` | component tag, children, component list | reviewed | dashboards.md |
| [Component - Layer](https://unfoldadmin.com/docs/components/layer/) | `components/layer.md` | layer wrapper | reviewed | dashboards.md |
| [Component - Link](https://unfoldadmin.com/docs/components/link/) | `components/link.md` | link params | reviewed | dashboards.md |
| [Component - Progress](https://unfoldadmin.com/docs/components/progress/) | `components/progress.md` | progress data shape | reviewed | dashboards.md |
| [Component - Table](https://unfoldadmin.com/docs/components/table/) | `components/table.md` | table data, nested tables | reviewed | dashboards.md |
| [Component - Tracker](https://unfoldadmin.com/docs/components/tracker/) | `components/tracker.md` | tracker data shape | reviewed | dashboards.md |

### configuration

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Avatar](https://unfoldadmin.com/docs/configuration/avatar/) | `configuration/avatar.md` | avatar_url / avatar_badge_* properties | reviewed | configuration.md |
| [Command](https://unfoldadmin.com/docs/configuration/command/) | `configuration/command.md` | COMMAND, SearchResult, history | reviewed | navigation.md |
| [Conditional fields](https://unfoldadmin.com/docs/configuration/conditional-fields/) | `configuration/conditional-fields.md` | conditional_fields, multiwidget suffixes | reviewed | model-admin.md |
| [Crispy Forms](https://unfoldadmin.com/docs/configuration/crispy-forms/) | `configuration/crispy-forms.md` | unfold_crispy pack, FormHelper, formsets | reviewed | forms-and-widgets.md |
| [Custom pages](https://unfoldadmin.com/docs/configuration/custom-pages/) | `configuration/custom-pages.md` | UnfoldModelAdminViewMixin, tab_list | reviewed | custom-pages-and-sites.md |
| [Custom sites](https://unfoldadmin.com/docs/configuration/custom-sites/) | `configuration/custom-sites.md` | UnfoldAdminSite, BasicAppConfig | reviewed | custom-pages-and-sites.md |
| [Dashboard](https://unfoldadmin.com/docs/configuration/dashboard/) | `configuration/dashboard.md` | admin/index.html, DASHBOARD_CALLBACK | reviewed | dashboards.md |
| [Datasets](https://unfoldadmin.com/docs/configuration/datasets/) | `configuration/datasets.md` | BaseDataset, change_form_datasets | reviewed | model-admin.md |
| [Configuration](https://unfoldadmin.com/docs/configuration/) | `configuration/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [ModelAdmin options](https://unfoldadmin.com/docs/configuration/modeladmin/) | `configuration/modeladmin.md` | ModelAdmin option table | reviewed | model-admin.md |
| [Multi-language](https://unfoldadmin.com/docs/configuration/multi-language/) | `configuration/multi-language.md` | SHOW_LANGUAGES, LANGUAGES override, i18n urls | reviewed | configuration.md |
| [Paginator](https://unfoldadmin.com/docs/configuration/paginator/) | `configuration/paginator.md` | InfinitePaginator | reviewed | model-admin.md |
| [Sections (Expandable rows)](https://unfoldadmin.com/docs/configuration/sections/) | `configuration/sections.md` | TableSection, TemplateSection, prefetch | reviewed | model-admin.md |
| [Settings options](https://unfoldadmin.com/docs/configuration/settings/) | `configuration/settings.md` | UNFOLD keys, SIDEBAR, TABS, COLORS, LOGIN, callbacks | reviewed | configuration.md; navigation.md; styling.md |
| [Site dropdown](https://unfoldadmin.com/docs/configuration/site-dropdown/) | `configuration/site-dropdown.md` | SITE_DROPDOWN | reviewed | navigation.md |
| [Sortable changelist](https://unfoldadmin.com/docs/configuration/sortable-changelist/) | `configuration/sortable-changelist.md` | ordering_field on changelist | reviewed | model-admin.md |

### decorators

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Action](https://unfoldadmin.com/docs/decorators/action/) | `decorators/action.md` | @action params, ActionVariant | reviewed | actions.md |
| [Display](https://unfoldadmin.com/docs/decorators/display/) | `decorators/display.md` | label, header, dropdown, formatting | reviewed | model-admin.md |
| [Decorators](https://unfoldadmin.com/docs/decorators/) | `decorators/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |

### development

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Development](https://unfoldadmin.com/docs/development/index/) | `development/index.md` | contributor dev server, tests, Tailwind build | reviewed | styling.md |

### fields

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Autocomplete fields](https://unfoldadmin.com/docs/fields/autocomplete/) | `fields/autocomplete.md` | autocomplete form fields, BaseAutocompleteView | reviewed | forms-and-widgets.md |
| [Fields](https://unfoldadmin.com/docs/fields/) | `fields/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [JsonField](https://unfoldadmin.com/docs/fields/json/) | `fields/json.md` | readonly JSON, Pygments, PrettyJSONEncoder | reviewed | model-admin.md |

### filters

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Autocomplete filter](https://unfoldadmin.com/docs/filters/autocomplete/) | `filters/autocomplete.md` | AutocompleteSelect(Multiple)Filter | reviewed | filters.md |
| [Checkbox and radio filters](https://unfoldadmin.com/docs/filters/checkbox-radio/) | `filters/checkbox-radio.md` | radio/checkbox/boolean/related/all-values filters | reviewed | filters.md |
| [Datetime filter](https://unfoldadmin.com/docs/filters/datetime/) | `filters/datetime.md` | RangeDateFilter, RangeDateTimeFilter | reviewed | filters.md |
| [Dropdown filter](https://unfoldadmin.com/docs/filters/dropdown/) | `filters/dropdown.md` | Choices/Related/Custom dropdown filters | reviewed | filters.md |
| [Horizontal layout filter](https://unfoldadmin.com/docs/filters/horizontal/) | `filters/horizontal.md` | horizontal attribute | reviewed | filters.md |
| [Filters](https://unfoldadmin.com/docs/filters/) | `filters/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [Introduction to filters](https://unfoldadmin.com/docs/filters/introduction/) | `filters/introduction.md` | contrib.filters, list_filter_submit, list_filter_options | reviewed | filters.md |
| [Numeric filter](https://unfoldadmin.com/docs/filters/numeric/) | `filters/numeric.md` | Single/Range/Slider/RangeNumericList filters | reviewed | filters.md |
| [Text filter](https://unfoldadmin.com/docs/filters/text/) | `filters/text.md` | TextFilter, FieldTextFilter | reviewed | filters.md |

### inlines

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Inlines](https://unfoldadmin.com/docs/inlines/) | `inlines/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [Introduction to inlines](https://unfoldadmin.com/docs/inlines/introduction/) | `inlines/introduction.md` | Unfold inline classes | reviewed | inlines.md |
| [Nested inlines](https://unfoldadmin.com/docs/inlines/nested/) | `inlines/nested.md` | nested inlines, limits | reviewed | inlines.md |
| [Nonrelated inlines](https://unfoldadmin.com/docs/inlines/nonrelated/) | `inlines/nonrelated.md` | NonrelatedTabular/StackedInline | reviewed | inlines.md |
| [Inline options](https://unfoldadmin.com/docs/inlines/options/) | `inlines/options.md` | show_count, get_inline_title, show_title, collapsible | reviewed | inlines.md |
| [Paginated inlines](https://unfoldadmin.com/docs/inlines/paginated/) | `inlines/paginated.md` | per_page, generic & nonrelated | reviewed | inlines.md |
| [Sortable inlines](https://unfoldadmin.com/docs/inlines/sortable/) | `inlines/sortable.md` | ordering_field on inlines | reviewed | inlines.md |

### installation

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [User & group models](https://unfoldadmin.com/docs/installation/auth/) | `installation/auth.md` | User/Group re-registration, unfold.forms | reviewed | configuration.md |
| [Installation](https://unfoldadmin.com/docs/installation/) | `installation/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [Quickstart](https://unfoldadmin.com/docs/installation/quickstart/) | `installation/quickstart.md` | INSTALLED_APPS order, contrib apps, ModelAdmin inheritance | reviewed | configuration.md |

### integrations

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [django-celery-beat](https://unfoldadmin.com/docs/integrations/django-celery-beat/) | `integrations/django-celery-beat.md` | re-register 5 admins | reviewed | integrations.md |
| [django-constance](https://unfoldadmin.com/docs/integrations/django-constance/) | `integrations/django-constance.md` | UNFOLD_CONSTANCE_ADDITIONAL_FIELDS | reviewed | integrations.md |
| [django-guardian](https://unfoldadmin.com/docs/integrations/django-guardian/) | `integrations/django-guardian.md` | contrib.guardian | reviewed | integrations.md |
| [django-hijack](https://unfoldadmin.com/docs/integrations/django-hijack/) | `integrations/django-hijack.md` | contrib.hijack | reviewed | integrations.md |
| [django-import-export](https://unfoldadmin.com/docs/integrations/django-import-export/) | `integrations/django-import-export.md` | Import/Export forms | reviewed | integrations.md |
| [django-json-widget](https://unfoldadmin.com/docs/integrations/django-json-widget/) | `integrations/django-json-widget.md` | CSS-only | reviewed | integrations.md |
| [django-location-field](https://unfoldadmin.com/docs/integrations/django-location-field/) | `integrations/django-location-field.md` | UnfoldAdminLocationWidget | reviewed | integrations.md |
| [django-modeltranslation](https://unfoldadmin.com/docs/integrations/django-modeltranslation/) | `integrations/django-modeltranslation.md` | deprecated 0.102, removed | reviewed | integrations.md |
| [django-money](https://unfoldadmin.com/docs/integrations/django-money/) | `integrations/django-money.md` | UnfoldAdminMoneyWidget auto | reviewed | integrations.md |
| [django-simple-history](https://unfoldadmin.com/docs/integrations/django-simple-history/) | `integrations/django-simple-history.md` | SimpleHistoryAdmin mixin | reviewed | integrations.md |
| [django-waffle](https://unfoldadmin.com/docs/integrations/django-waffle/) | `integrations/django-waffle.md` | Unfold FlagAdmin | reviewed | integrations.md |
| [djangoql](https://unfoldadmin.com/docs/integrations/djangoql/) | `integrations/djangoql.md` | CSS-only | reviewed | integrations.md |
| [Integrations](https://unfoldadmin.com/docs/integrations/) | `integrations/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |

### styles-scripts

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Customizing Tailwind stylesheet](https://unfoldadmin.com/docs/styles-scripts/customizing-tailwind/) | `styles-scripts/customizing-tailwind.md` | Tailwind 4 / 3 setup | reviewed | styling.md |
| [Styles & scripts](https://unfoldadmin.com/docs/styles-scripts/) | `styles-scripts/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [Loading styles and scripts](https://unfoldadmin.com/docs/styles-scripts/loading-files/) | `styles-scripts/loading-files.md` | STYLES, SCRIPTS | reviewed | styling.md |

### tabs

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [Changeform tabs](https://unfoldadmin.com/docs/tabs/changeform/) | `tabs/changeform.md` | TABS detail=True | reviewed | navigation.md |
| [Changelist tabs](https://unfoldadmin.com/docs/tabs/changelist/) | `tabs/changelist.md` | TABS models list | reviewed | navigation.md |
| [Dynamic tabs](https://unfoldadmin.com/docs/tabs/dynamic/) | `tabs/dynamic.md` | TABS callback, page, tab_list, inline, active | reviewed | navigation.md |
| [Fieldsets tabs](https://unfoldadmin.com/docs/tabs/fieldsets/) | `tabs/fieldsets.md` | fieldset 'tab' class | reviewed | model-admin.md |
| [Tabs](https://unfoldadmin.com/docs/tabs/) | `tabs/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [Inlines tabs](https://unfoldadmin.com/docs/tabs/inline/) | `tabs/inline.md` | inline tab=True | reviewed | inlines.md |

### widgets

| Page | Path | Key concepts / APIs | Status | Incorporated in |
|---|---|---|---|---|
| [ArrayWidget](https://unfoldadmin.com/docs/widgets/array/) | `widgets/array.md` | ArrayWidget, choices | reviewed | forms-and-widgets.md |
| [Widgets](https://unfoldadmin.com/docs/widgets/) | `widgets/index.md` | Section index (navigation only) | n/a: no content | SKILL.md (section) |
| [WysiwygWidget](https://unfoldadmin.com/docs/widgets/wysiwyg/) | `widgets/wysiwyg.md` | WysiwygWidget (Trix) | reviewed | forms-and-widgets.md |

### Known live pages missing from the snapshot

| Page | URL | Status | Interim coverage |
|---|---|---|---|
| django-reversion | https://unfoldadmin.com/docs/integrations/django-reversion/ | inaccessible (added after snapshot, v0.109.0) | integrations.md: app name and ordering from source and test settings |
| django-reversion-compare | https://unfoldadmin.com/docs/integrations/django-reversion-compare/ | inaccessible (added after snapshot, v0.109.0) | integrations.md: app name and ordering from source and test settings |

## Post-snapshot features (v0.106 to v0.110), from the changelog and source

None of these were documented in the snapshot. The live site may document them.

| Version | Feature | Covered in | Basis |
|---|---|---|---|
| 0.106.0 | Card `title_icon` and `description` | dashboards.md | template diff |
| 0.106.0 | Constance date, time and datetime fields | integrations.md | changelog |
| 0.107.0 | Related-object modals (`xframe_options_sameorigin` on views) | not covered (automatic UI behaviour) | changelog |
| 0.108.0 | `JSONSchemaField` / `UnfoldAdminJSONSchemaField` | forms-and-widgets.md | source and tests |
| 0.109.0 | Sidebar sub-navigation (`items` on an item) | navigation.md | template and tests |
| 0.109.0 | django-reversion and django-reversion-compare | integrations.md | source |
| 0.110.0 | Python 3.15 | SKILL.md, README | pyproject |

## Undocumented settings present in v0.110.0 `CONFIG_DEFAULTS`

`GLOBAL_CALLBACK`, `ACCOUNT.navigation`, `LANGUAGE_FLAGS` and `FORMS.classes` are listed in configuration.md and flagged as undocumented.

## Unresolved questions

1. Whether the live docs now differ from the 2026-09-05 snapshot beyond the two reversion pages.
2. The exact supported `SITE_VIEWS` view contract. Only the settings shape is documented; the behaviour comes from source.
3. Whether `unfold/layouts/base.html` or `admin/base.html` is the preferred base for custom pages. The docs prose and examples disagree; the skill follows the examples.

## How to update

1. Get the current docs. If you can reach unfoldadmin.com, compare its navigation with the inventory above.
2. For each new or changed page, update the mapped reference file and this table.
3. Re-verify imports against the new release's source, then bump the versions in `SKILL.md` metadata, README and CHANGELOG.
4. Run `python scripts/validate.py`.

