# Actions

Docs: [introduction](https://unfoldadmin.com/docs/actions/introduction/) · [changelist](https://unfoldadmin.com/docs/actions/changelist/) · [row](https://unfoldadmin.com/docs/actions/changelist-row/) · [changeform](https://unfoldadmin.com/docs/actions/changeform/) · [submit line](https://unfoldadmin.com/docs/actions/changeform-submitline/) · [dropdown](https://unfoldadmin.com/docs/actions/dropdown-actions/) · [dialog](https://unfoldadmin.com/docs/actions/dialog-actions/) · [form example](https://unfoldadmin.com/docs/actions/action-form-example/) · [@action](https://unfoldadmin.com/docs/decorators/action/)

Unfold actions extend Django admin actions. Always decorate them with `unfold.decorators.action`.

## Pick the action type

| Attribute | Where it shows | Handler signature | Dropdown groups |
|---|---|---|---|
| `actions` (Django) | Bulk dropdown | `(self, request, queryset)` | n/a |
| `actions_list` | Changelist top, as buttons | `(self, request)`, with **no queryset** | yes |
| `actions_row` | Each changelist row (dropdown) | `(self, request, object_id)` | no |
| `actions_detail` | Changeform top | `(self, request, object_id)` | yes |
| `actions_submit_line` | Next to Save | `(self, request, obj)`, run **after** save | no |

- List, row and detail actions each get their own URL, named `admin:<app>_<model>_<method_name>`. The path is `<url_path or method_name>/`, prefixed with `<object_id>/` for row and detail actions. The handler is effectively a function-based view and should return a response, usually `redirect(...)` back to where it was triggered.
- For multi-step flows, have the handler redirect to a custom view. See [custom-pages-and-sites.md](custom-pages-and-sites.md).
- Submit-line actions receive the already saved instance. If you change it, call `obj.save()` again.
  - They run in `save_model` when the POST contains the button name `<app>_<model>_<method>`.
  - Set `attrs={"name": ...}` to change that name.

## `@action` parameters

| Param | Meaning |
|---|---|
| `description` | Button text |
| `url_path` | URL segment; generated if omitted |
| `attrs` | HTML attrs on the `<a>`, e.g. `{"target": "_blank"}` |
| `icon` | Material Symbols name |
| `variant` | `unfold.enums.ActionVariant`: `DEFAULT PRIMARY SUCCESS INFO WARNING DANGER` |
| `permissions` | `["name"]` calls `has_name_permission`; `["app.codename"]` checks a Django perm |
| `dialog` | Confirmation dialog (below) |

```python
from django.shortcuts import redirect
from django.urls import reverse_lazy
from unfold.admin import ModelAdmin
from unfold.decorators import action
from unfold.enums import ActionVariant

@admin.register(User)
class UserAdmin(ModelAdmin):
    actions_list = ["sync"]
    actions_row = ["open_profile"]
    actions_detail = ["block"]
    actions_submit_line = ["activate"]

    @action(description=_("Sync"), icon="sync", url_path="sync", permissions=["sync"])
    def sync(self, request):
        return redirect(reverse_lazy("admin:auth_user_changelist"))

    def has_sync_permission(self, request):
        return request.user.is_superuser

    @action(description=_("Profile"), url_path="profile", attrs={"target": "_blank"})
    def open_profile(self, request, object_id):
        return redirect(reverse_lazy("admin:auth_user_change", args=[object_id]))

    @action(description=_("Block"), variant=ActionVariant.DANGER, permissions=["block"])
    def block(self, request, object_id):
        ...
        return redirect(reverse_lazy("admin:auth_user_change", args=[object_id]))

    def has_block_permission(self, request, object_id):   # detail: receives object_id
        return True

    @action(description=_("Save and activate"))
    def activate(self, request, obj):
        obj.is_active = True
        obj.save()
```

## Permission rules

- `has_<name>_permission(self, request, ...)` is defined on the ModelAdmin.
  - Detail and submit-line actions receive `object_id`.
  - **Row actions do not**, so per-row permissions are impossible.
  - List actions receive only `request`.
- A string containing a dot is a Django permission. On detail views it is checked without the object.
- Method-based and dotted permissions can be mixed in one list.

## Dropdown groups (`actions_list`, `actions_detail` only)

```python
actions_list = ["a1", {"title": _("More"), "icon": "person", "items": ["a2", "a3"]}]
```

A group whose items all fail permissions is hidden.

## Hiding default actions

```python
actions_list_hide_default = True     # and/or actions_detail_hide_default
```

Re-expose a hidden default by wrapping it in your own `@action` that redirects to the original URL.

## Dialog actions (confirmation modal, HTMX)

```python
from django.http import HttpResponse
from unfold.forms import BaseDialogForm

class ReasonForm(BaseDialogForm):             # MUST inherit BaseDialogForm, not forms.Form
    reason = forms.CharField(label=_("Reason"))
    form_before_template = "app/before.html"   # optional
    form_after_template = "app/after.html"
    def get_before_template_context(self, request, object_id):   # drop object_id for list actions
        return {"obj_id": object_id}
    def clean_reason(self):
        self.request                            # request is available
        return self.cleaned_data["reason"]

class OrderAdmin(ModelAdmin):
    actions_list = ["bulk_close"]
    actions_row = ["close"]

    @action(description=_("Close all"), dialog={
        "title": _("Close all"), "description": _("Are you sure?"),
        "form_submit_text": _("Close"),         # docs say "submit_text"; v0.110 reads form_submit_text
        "form_class": ReasonForm,               # optional
    })
    def bulk_close(self, request, form):        # list: (request, form)
        do_something(form.cleaned_data["reason"])
        messages.success(request, _("Done"))
        return HttpResponse(headers={"HX-Redirect": reverse_lazy("admin:app_order_changelist")})

    @action(description=_("Close"), dialog={"title": _("Close"), "description": "..."})
    def close(self, request, form, object_id):  # row and detail: (request, form, object_id)
        ...
```

- The dialog form must validate before the handler runs. A form with no fields is still present.
- `BaseDialogForm` carries a required hidden `_form_submitted` field. Keep it if you render the form yourself.
- Finish with an `HX-Redirect` header, not a plain redirect.

## Action with an intermediate form page (detail action)

Render a template that extends `admin/base_site.html` and pass `**self.admin_site.each_context(request)`. Use Unfold widgets in the form, and include `{{ form.media }}` and `admin:jsi18n`.

```python
class SomeForm(forms.Form):
    start = forms.SplitDateTimeField(widget=UnfoldAdminSplitDateTimeWidget)
    note = forms.CharField(widget=UnfoldAdminTextInputWidget)

@action(description=_("Change"), url_path="change-detail-action")
def change_detail_action(self, request, object_id):
    obj = get_object_or_404(User, pk=object_id)
    form = SomeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        messages.success(request, _("Done"))
        return redirect(reverse_lazy("admin:auth_user_change", args=[object_id]))
    return render(request, "app/action.html", {
        "form": form, "object": obj, "title": _("Change {}").format(obj),
        **self.admin_site.each_context(request)})
```

```django
{% extends "admin/base_site.html" %}
{% load i18n unfold %}
{% block extrahead %}{{ block.super }}<script src="{% url 'admin:jsi18n' %}"></script>{{ form.media }}{% endblock %}
{% block content %}
<form method="post" novalidate>{% csrf_token %}
  {% for field in form %}{% include "unfold/helpers/field.html" with field=field %}{% endfor %}
  {% component "unfold/components/button.html" with submit=1 %}{% trans "Submit" %}{% endcomponent %}
</form>
{% endblock %}
```

- Date widgets need the admin JS: jQuery, `jquery.init.js`, `calendar.js`, `DateTimeShortcuts.js` and `core.js`. Load them in the form's `Media.js`.
- Breadcrumbs are not provided. Build your own if needed.
