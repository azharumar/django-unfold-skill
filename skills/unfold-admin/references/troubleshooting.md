# Troubleshooting

Symptom, then cause, then fix. Each row links to the reference file with the details.

| Symptom | Likely cause | Fix |
|---|---|---|
| Admin looks like stock Django | `"unfold"` is listed after `django.contrib.admin`, or missing | Put `"unfold"` first ([configuration.md](configuration.md)) |
| One model's pages are unstyled, or Unfold options are ignored | Its admin inherits `django.contrib.admin.ModelAdmin` | Inherit `unfold.admin.ModelAdmin` |
| User or Group pages unstyled; password form broken | Default auth admins are still registered | Unregister and re-register with `unfold.forms` ([configuration.md](configuration.md#user-and-group-admin-always-needed-with-djangocontribauth)) |
| Third-party admin pages unstyled (celery-beat, waffle, …) | The package registers plain Django admins | Unregister and re-register with `ModelAdmin` mixed in ([integrations.md](integrations.md)) |
| `NoReverseMatch` on a custom site | Site subclasses `AdminSite` | Subclass `unfold.sites.UnfoldAdminSite` ([custom-pages-and-sites.md](custom-pages-and-sites.md)) |
| `default_site` override has no effect | `"unfold"` app config overrides `admin.site` | Use `"unfold.apps.BasicAppConfig"` |
| Models disappear from the sidebar | `SIDEBAR.navigation` replaces the automatic app list | Link every needed model, or enable `show_all_applications` ([navigation.md](navigation.md)) |
| Custom page missing from the menu | Custom views are never auto-added | Add a `SIDEBAR` item |
| Sidebar item (or sub-navigation parent) silently missing | Item has no `link` | Give every item a `link` |
| Custom ModelAdmin URL redirects to `.../change/` | Appended after `super().get_urls()`, so the catch-all matches first | Prepend: `[path(...)] + super().get_urls()` |
| Paginated inline warns `UnorderedObjectListWarning` | Inline model has no ordering | Add `Meta.ordering`, or order the inline queryset |
| Custom page errors or has no Unfold chrome | Missing `model_admin=self`, `title` or `permission_required`, or the template does not extend `admin/base.html` | See [custom-pages-and-sites.md](custom-pages-and-sites.md) |
| A setting shows a dotted path as literal text | A dotted string that fails to import silently falls back to the raw string (`UnfoldAdminSite._get_value`) | Fix the import path and make sure the target is importable |
| Settings crash at import with URL or translation errors | `reverse()` or `gettext()` used in settings | Use `reverse_lazy` and `gettext_lazy`, or lambdas |
| Input filter has no way to apply | `list_filter_submit` is not set | `list_filter_submit = True` ([filters.md](filters.md)) |
| Errors with special filters | `unfold.contrib.filters` not installed, or autocomplete target lacks `search_fields` | Install the app, and add `search_fields` to the related admin |
| Dropdown filter slow or huge | Related dropdowns load every object | Use `AutocompleteSelectFilter` |
| Sections make many queries | One query per row for the related table | `prefetch_related` in `get_queryset` ([model-admin.md](model-admin.md#sections-expandable-changelist-rows)) |
| Dataset shows other parents' rows, or crashes on the add page | Unscoped queryset | Filter on `self.extra_context.get("object")` and return `.none()` when it is missing |
| `list_filter` on a dataset ignored | Not supported | Remove it; use search |
| Row action permission cannot see the object | Row permission methods get no `object_id` | Use a detail action, or check inside the handler |
| Submit-line action changes are lost | The handler runs after save | Call `obj.save()` again |
| Dialog action does not redirect | Returned a normal redirect | Return `HttpResponse(headers={"HX-Redirect": url})` ([actions.md](actions.md#dialog-actions-confirmation-modal-htmx)) |
| Dialog form misbehaves | Form subclasses `forms.Form` | Subclass `unfold.forms.BaseDialogForm` |
| Dialog submit button ignores the custom label | Used the docs' `submit_text` key | Use `form_submit_text` |
| Plain form inputs unstyled on custom pages | Django default widgets | Use `unfold.widgets.*` ([forms-and-widgets.md](forms-and-widgets.md)) |
| Date picker missing in a custom form | Admin JS and `jsi18n` not loaded | Add `Media.js` and the `admin:jsi18n` script |
| `ArrayWidget` ignores choices | The widget does not read model choices | Pass `choices=` in `get_form` |
| Custom Tailwind classes have no effect | Unfold's CSS has only its own classes | Write plain CSS or compile Tailwind 4, then load with `STYLES` ([styling.md](styling.md)) |
| Tailwind 3 colour config broken | `rgb(var(--color-*))` mapping applies to Unfold below 0.56 only | Use Tailwind 4 or plain CSS with `var(--color-primary-600)` |
| `hide_title` has no effect on an inline | Renamed in v0.104.0 | Use `show_title = False`; StackedInline also needs `can_delete = False` |
| Sort handle missing on new inline rows | Rows must be saved first | Save, then reorder |
| Third inline level ignored | Only one nested level is supported | Flatten the structure |
| Readonly JSON not highlighted | Pygments not installed, or field is not readonly | `pip install pygments`; add the field to `readonly_fields` |
| `ImportError: unfold.contrib.import_export.admin` | Removed | Use import-export 4.x `ExportActionModelAdmin` directly |
| modeltranslation tabs or flags gone | Support deprecated in v0.102.0 and removed | No Unfold replacement is documented |
| Command search hits the database hard | `search_models=True` searches every model | Pass a list, or a callback |
| Tabs never show as active on a custom page | Unfold cannot detect it | Set `"active"` on the tab item |

## Known errors in official docs examples

Do not copy these verbatim:

| Page | Problem | Correct form |
|---|---|---|
| configuration/command | `SearchResult("title": ...)` | `SearchResult(title=..., description=..., link=..., icon=...)` |
| configuration/conditional-fields | No commas between dict items | Add commas |
| filters/dropdown | `(...)(...)` tuple call | Separate the tuples with a comma |
| filters/numeric | `super().get_queryset()` | `super().get_queryset(request)` |
| fields/autocomplete | Queryset-narrowing `__init__` shown on the view; `custon_` typo | It belongs on the form; use a consistent URL name |
| configuration/crispy-forms | `from crispy_forms.layout` incomplete import | Remove it, or import what is needed |
| components/button, components/tracker | Missing `{` and missing comma | Fix the syntax |
| components/progress | `progress-class` | `progress_class` (template key) |
| components/introduction | `unfold/components/cohort.html` | `unfold/components/chart/cohort.html` |
| tabs/dynamic | Prose says `is_active` | The key is `active`; the docs callback also wraps its list in a tuple |
| configuration/custom-sites | `get_urls` on `AdminConfig` | Define it on the `UnfoldAdminSite` subclass |
| inlines/sortable | "not available in changelist" | Superseded by the sortable-changelist page |
| configuration/modeladmin | `from django import models` | `from django.db import models` |
| configuration/custom-pages | `super().get_urls() + [custom]` | `[custom] + super().get_urls()` |
| actions/dialog-actions | `dialog={"submit_text": ...}` | `dialog={"form_submit_text": ...}` (key read by v0.110 source) |
