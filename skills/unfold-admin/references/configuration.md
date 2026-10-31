# Installation and `UNFOLD` settings

Covers: installation, `INSTALLED_APPS`, the `UNFOLD` dict, branding, login, environment label, user and group admin, avatar, multi-language. Navigation keys (`SIDEBAR`, `TABS`, `COMMAND`, `SITE_DROPDOWN`) are in [navigation.md](navigation.md). Colours and assets are in [styling.md](styling.md).

Docs: [quickstart](https://unfoldadmin.com/docs/installation/quickstart/) · [settings](https://unfoldadmin.com/docs/configuration/settings/) · [auth](https://unfoldadmin.com/docs/installation/auth/) · [avatar](https://unfoldadmin.com/docs/configuration/avatar/) · [multi-language](https://unfoldadmin.com/docs/configuration/multi-language/)

## Install

```bash
pip install django-unfold        # or: uv add django-unfold / poetry add django-unfold
```

```python
INSTALLED_APPS = [
    "unfold",                          # MUST come before django.contrib.admin
    "unfold.contrib.filters",          # special list filters
    "unfold.contrib.forms",            # ArrayWidget, WysiwygWidget
    "unfold.contrib.inlines",          # nonrelated inlines
    "unfold.contrib.import_export",    # django-import-export
    "unfold.contrib.guardian",         # django-guardian
    "unfold.contrib.simple_history",   # django-simple-history
    "unfold.contrib.location_field",   # django-location-field
    "unfold.contrib.constance",        # django-constance
    "unfold.contrib.hijack",           # django-hijack
    "django.contrib.admin",
]
```

- Add only the contrib apps you use. Put `unfold.contrib.filters` straight after `unfold`.
- `urls.py` stays `path("admin/", admin.site.urls)`.
- Every admin class must inherit `unfold.admin.ModelAdmin`. A plain Django `ModelAdmin` renders unstyled and has none of the Unfold options.
- To override the default site through `AdminConfig.default_site`, install `"unfold.apps.BasicAppConfig"` instead of `"unfold"`. See [custom-pages-and-sites.md](custom-pages-and-sites.md).

## User and Group admin (always needed with `django.contrib.auth`)

```python
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

## Value conventions in `UNFOLD`

- **Callable**: `lambda request: ...`. Used for URLs and static paths such as `SITE_ICON`, `STYLES` and `LOGIN.image`.
- **Dotted string**: `"app.module.func"`, imported and called. Used for `ENVIRONMENT`, `DASHBOARD_CALLBACK`, badges and permissions. Permission keys also accept lambdas.
- Use `reverse_lazy` for admin URLs and `gettext_lazy` for titles, because settings load before URLconf and translations.

## Top-level keys

| Key | Value | Notes |
|---|---|---|
| `SITE_TITLE` | str | Suffix of `<title>` |
| `SITE_HEADER` / `SITE_SUBHEADER` | str | Sidebar top text |
| `SITE_VERSION` | str | Shown as plain text |
| `SITE_URL` | str | Default `"/"` |
| `SITE_ICON` / `SITE_LOGO` | callable, or `{"light": cb, "dark": cb}` | Optimise for 32px height |
| `SITE_SYMBOL` | Material Symbols name | e.g. `"speed"` |
| `SITE_FAVICONS` | list of `{"rel","sizes","type","href": cb}` | |
| `SITE_DROPDOWN` | list | See navigation.md |
| `SITE_VIEWS` | list of `(path, name, "dotted.view")` | Registers extra views on the site |
| `SHOW_HISTORY` | bool, default True | "History" button |
| `SHOW_VIEW_ON_SITE` | bool, default True | |
| `SHOW_BACK_BUTTON` | bool, default False | Changeform header |
| `SHOW_UI_WARNINGS` | bool, default False | |
| `SHOW_LANGUAGES` | bool, default False | Language selector |
| `ENVIRONMENT` | dotted callback returning `[label, variant]` | Variant is one of `info`, `danger`, `warning`, `success` |
| `ENVIRONMENT_TITLE_PREFIX` | dotted callback | Prefix in `<title>` |
| `DASHBOARD_CALLBACK` | dotted `fn(request, context) -> context` | See dashboards.md |
| `THEME` | `"dark"` or `"light"` | Forces the theme and removes the switcher |
| `BORDER_RADIUS`, `COLORS`, `STYLES`, `SCRIPTS` | | See styling.md |
| `LOGIN` | `{"image": cb, "redirect_after": cb, "form": "dotted.Form"}` | The form must inherit `unfold.forms.AuthenticationForm` |
| `SIDEBAR`, `TABS`, `COMMAND`, `LANGUAGES` | | See navigation.md and below |

```python
def environment_callback(request):
    return ["Production", "danger"]
```

### In the v0.110.0 source but not in the docs snapshot

These are verified to exist in the code but are undocumented, so treat them as unstable. Use them only if the user asks.
- `GLOBAL_CALLBACK`: a dotted `fn(request) -> dict`, merged into every admin page context.
- `ACCOUNT = {"navigation": [{"title", "link"}]}`: extra links in the user menu.
- `LANGUAGE_FLAGS`: a dict passed to templates.
- `FORMS = {"classes": {...}}`: overrides widget CSS class strings.

## Avatar (user model properties)

```python
class User(AbstractUser):
    @property
    def avatar_url(self) -> str: return static("img/avatar.webp")
    @property
    def avatar_badge_variant(self) -> str | None: return "primary"  # danger warning success info primary default
    @property
    def avatar_badge_count(self) -> str | int | None: return 3
    @property
    def avatar_badge_url(self) -> str | None: return "/admin/"
```

## Multi-language

1. Add `django.middleware.locale.LocaleMiddleware`, set `USE_I18N = True`, and set `LANGUAGE_CODE` and `LANGUAGES`.
2. In `urls.py`, put `path("i18n/", include("django.conf.urls.i18n"))` **outside** `i18n_patterns`. Put admin inside: `i18n_patterns(path("admin/", admin.site.urls))`.
3. Set `UNFOLD["SHOW_LANGUAGES"] = True`. The selector appears top right.
4. Optionally override the list. Each item has the shape of `django.utils.translation.get_language_info`:

```python
"LANGUAGES": {
    "navigation": [{"bidi": False, "code": "de", "name": "German", "name_local": "Deutsch", "name_translated": "German"}],
    # or "navigation": "app.utils.languages_callback"   -> fn(request) -> list
    # "action": reverse_lazy("custom_form_submit")       # custom language-switch endpoint
},
```
