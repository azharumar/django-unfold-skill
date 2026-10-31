# Navigation: sidebar, tabs, site dropdown, command palette

Docs: [settings](https://unfoldadmin.com/docs/configuration/settings/) · [site dropdown](https://unfoldadmin.com/docs/configuration/site-dropdown/) · [command](https://unfoldadmin.com/docs/configuration/command/) · [changelist tabs](https://unfoldadmin.com/docs/tabs/changelist/) · [changeform tabs](https://unfoldadmin.com/docs/tabs/changeform/) · [dynamic tabs](https://unfoldadmin.com/docs/tabs/dynamic/)

Fieldset tabs and inline tabs live in the admin class, not in settings. See [model-admin.md](model-admin.md#fieldset-tabs) and [inlines.md](inlines.md).

## Sidebar: `UNFOLD["SIDEBAR"]`

```python
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {"SIDEBAR": {
    "show_search": False,            # search app and model names
    "show_all_applications": False,  # dropdown listing every app and model
    "navigation": [
        {
            "title": _("Navigation"),
            "separator": True,       # top border
            "collapsible": True,     # group can collapse
            "items": [
                {
                    "title": _("Dashboard"),
                    "icon": "dashboard",                    # Material Symbols name
                    "icon_template": "helpers/icon/x.svg",  # optional custom icon template
                    "link": reverse_lazy("admin:index"),
                    "link_attrs": {"target": "_blank"},
                    "badge": "app.utils.badge_callback",    # fn(request) -> value
                    "badge_variant": "info",                # info success warning primary danger
                    "badge_style": "solid",
                    "badge_class": "ml-auto",
                    "permission": lambda request: request.user.is_superuser,
                },
                {"title": _("Users"), "icon": "people", "link": reverse_lazy("admin:auth_user_changelist")},
            ],
        },
    ],
}}
```

- Once `navigation` is set, it **replaces** the automatic app list. Every model the user needs must be linked by hand.
- `permission` takes a dotted path or a callable `fn(request) -> bool`. Items that fail it are hidden.
- Custom views are **never** added automatically. Link them here.
- Admin URL names follow `admin:<app_label>_<model>_changelist`, `_add` and `_change`.
- Icons come from [Material Symbols](https://fonts.google.com/icons). Use the ligature name.

- **Every item needs a `link`.** Items without one are silently dropped (`UnfoldAdminSite._get_navigation_items`).

**Since the docs snapshot (verified in v0.110.0 source and tests, undocumented):**
- An item may carry its own `"items": [...]` list of `{title, link, permission?, active?}`. That renders a collapsible sub-navigation (v0.109.0).
- The parent still needs a `link`, or it is dropped, but it acts only as the toggle.
- `SIDEBAR` may also be a dotted callback returning the dict.

## Site dropdown: `UNFOLD["SITE_DROPDOWN"]`

Opens when the site header is clicked. A dropdown icon appears automatically.

```python
"SITE_DROPDOWN": [
    {"icon": "diamond", "title": _("My site"), "link": "https://example.com", "attrs": {"target": "_blank"}},
    {"icon": "diamond", "title": _("Admin"), "link": reverse_lazy("admin:index")},
],
```

## Tabs: `UNFOLD["TABS"]`

The tab bar sits above the changelist or changeform of the listed models.

```python
"TABS": [
    {
        "models": [
            "app_label.modelname",                          # changelist tabs
            {"name": "app_label.other", "detail": True},    # changeform tabs
        ],
        "items": [
            {"title": _("All"), "link": reverse_lazy("admin:app_label_modelname_changelist"),
             "permission": "app.utils.permission_callback"},
            {"title": _("Other"), "link": reverse_lazy("admin:app_label_other_changelist")},
        ],
    },
],
```

- Model names are written as `app_label.model_name_in_lowercase`.
- Item keys: `title`, `link` (a value or callable), `permission`, `active` (a bool or `fn(request)`; detected automatically from the URL when omitted), and `inline`.
- `"inline": "<fragment>"` links a tab to an inline on the changeform. The fragment is normally the slugified `verbose_name` of the inline model.

### Dynamic tabs and custom pages

```python
"TABS": "project.admin.tabs_callback"   # fn(request) -> list[dict] with the structure above
```

To show tabs on a custom page, give the group a unique `"page": "custom_page"`. Then call it from the template:

```django
{% load unfold %}
{% tab_list "custom_page" %}
```

On custom pages Unfold cannot detect which tab is active, so set `"active"` yourself. The docs prose says `is_active`, but the code reads `active`.

## Command palette: `UNFOLD["COMMAND"]`

Opens with Cmd+K (macOS) or Ctrl+K. By default it searches only app and model names.

```python
"COMMAND": {
    "search_models": True,                 # or ["app.model", ...] or "dotted.callback" -> list
    "search_callback": "app.utils.search_callback",
    "show_history": True,                  # stored in browser localStorage
},
```

- Searching model data needs `search_fields` on each model admin, and it queries every searchable model, which is heavy on the database. Restrict it with a list or a callback.
- Results load with infinite scroll, 100 per page.
- `show_history` stores queries in `localStorage`. Weigh that against data sensitivity.
- `search_callback(request, search_term)` returns extra results. **You must apply permissions yourself.**

```python
from unfold.dataclasses import SearchResult

def search_callback(request, search_term):
    return [SearchResult(title="Some title", description="Extra", link="https://example.com", icon="database")]
```

The docs example wraps dict syntax inside `SearchResult(...)`, which is invalid Python. `SearchResult` is a dataclass, so pass keyword arguments as above.
