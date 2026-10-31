# Custom pages and custom admin sites

Docs: [custom pages](https://unfoldadmin.com/docs/configuration/custom-pages/) · [custom sites](https://unfoldadmin.com/docs/configuration/custom-sites/)

## Custom page inside the admin UI

```python
from django.urls import path
from django.views.generic import TemplateView
from unfold.admin import ModelAdmin
from unfold.views import UnfoldModelAdminViewMixin

class ReportView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Report"                       # required: page header
    permission_required = ()               # required: tuple of permission strings
    template_name = "app/report.html"

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    def get_urls(self):
        view = self.admin_site.admin_view(ReportView.as_view(model_admin=self))   # model_admin is REQUIRED
        return [path("report/", view, name="order_report")] + super().get_urls()   # custom first
```

**Put custom URLs before `super().get_urls()`.**
- The docs append them (`super().get_urls() + [...]`).
- Django's catch-all `<path:object_id>/` pattern then matches first, and `report/` redirects to `report/change/`.
- Verified on Unfold 0.110.0 with Django 6.1.

```django
{% extends "admin/base.html" %}
{% load admin_urls i18n unfold %}
{% block content %}
  {% tab_list "orders" %}          {# optional; needs a TABS group with "page": "orders" #}
  ...
{% endblock %}
```

- The template extends `admin/base.html`. The docs prose also names `unfold/layouts/base.html`, which exists, but every docs example uses `admin/base.html`.
- **Breadcrumbs are not included** (removed in v0.64). Build them yourself if needed.
- **The page is not added to the sidebar.** Add a `SIDEBAR` item, using `reverse_lazy("admin:order_report")`.
- `FormView` works the same way. See the crispy example in [forms-and-widgets.md](forms-and-widgets.md#crispy-forms-unfold_crispy-template-pack).
- Alternatives:
  - `ModelAdmin.custom_urls = ((path, name, view),)` registers views under `admin:`.
  - `UNFOLD["SITE_VIEWS"] = [(path, name, "dotted.ViewClass")]` registers site-level views (v0.99.0+).
    - The docs give only the settings shape.
    - In the v0.110.0 source the class is built with `.as_view(admin_site=site)` and wrapped in `admin_site.admin_view`. So it must be a class-based view with an `admin_site` attribute, and it gets login protection only.
    - Add finer permission checks yourself.

## Custom admin site

```python
# sites.py
from unfold.sites import UnfoldAdminSite

class CustomAdminSite(UnfoldAdminSite):
    pass

custom_admin_site = CustomAdminSite(name="custom_admin_site")

# urls.py
path("admin/", custom_admin_site.urls)

# admin.py
@admin.register(User, site=custom_admin_site)
class UserAdmin(ModelAdmin):
    ...
```

**Always subclass `UnfoldAdminSite`.** A plain `django.contrib.admin.AdminSite` raises `NoReverseMatch`, because the URL patterns Unfold needs are missing.

## Replacing the default `admin.site`

1. In `INSTALLED_APPS`, use `"unfold.apps.BasicAppConfig"` instead of `"unfold"`. `BasicAppConfig` does not override `django.contrib.admin.site`.
2. Replace `"django.contrib.admin"` with your own `AdminConfig` subclass that has `default_site = "project.sites.CustomAdminSite"`. Replacing the default admin app this way is standard Django.

The docs example defines `get_urls` and `admin_view` on the `AdminConfig`. Those are `AdminSite` methods, so put extra URLs on your `UnfoldAdminSite` subclass.
