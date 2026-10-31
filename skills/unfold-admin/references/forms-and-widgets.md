# Forms, widgets and fields

Docs: [ArrayWidget](https://unfoldadmin.com/docs/widgets/array/) · [WysiwygWidget](https://unfoldadmin.com/docs/widgets/wysiwyg/) · [autocomplete fields](https://unfoldadmin.com/docs/fields/autocomplete/) · [crispy forms](https://unfoldadmin.com/docs/configuration/crispy-forms/) · [JSON field](https://unfoldadmin.com/docs/fields/json/)

## When you need to choose widgets by hand

- **ModelAdmin forms:** `unfold.admin.ModelAdmin` maps model fields to Unfold widgets automatically. Override only to change behaviour, for example `formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}`.
- **Plain `forms.Form` or `ModelForm`** used in custom pages, action forms, dialogs or crispy: set Unfold widgets explicitly, otherwise the inputs are unstyled.

Widgets in `unfold.widgets` (class names from the v0.110.0 source):

| Kind | Classes |
|---|---|
| Text | `UnfoldAdminTextInputWidget`, `UnfoldAdminEmailInputWidget`, `UnfoldAdminURLInputWidget`, `UnfoldAdminUUIDInputWidget`, `UnfoldAdminColorInputWidget`, `UnfoldAdminPasswordWidget`, `UnfoldAdminPasswordToggleWidget` |
| Text area | `UnfoldAdminTextareaWidget`, `UnfoldAdminExpandableTextareaWidget` |
| Numbers | `UnfoldAdminIntegerFieldWidget`, `UnfoldAdminBigIntegerFieldWidget`, `UnfoldAdminDecimalFieldWidget`, `UnfoldAdminIntegerRangeWidget` |
| Date and time | `UnfoldAdminSingleDateWidget`, `UnfoldAdminSingleTimeWidget`, `UnfoldAdminDateWidget`, `UnfoldAdminTimeWidget`, `UnfoldAdminSplitDateTimeWidget` (pair with `forms.SplitDateTimeField`), `UnfoldAdminSplitDateTimeVerticalWidget` |
| Choice | `UnfoldAdminSelectWidget`, `UnfoldAdminSelectMultipleWidget`, `UnfoldAdminRadioSelectWidget`, `UnfoldAdminCheckboxSelectMultipleWidget`, `UnfoldAdminNullBooleanSelectWidget` |
| Boolean | `UnfoldBooleanSwitchWidget` (default for `BooleanField`), `UnfoldBooleanWidget` |
| Files | `UnfoldAdminFileFieldWidget`, `UnfoldAdminImageFieldWidget`, `UnfoldAdminImageSmallFieldWidget` |
| Integrations | `UnfoldAdminMoneyWidget` (django-money), `UnfoldAdminLocationWidget` (django-location-field) |

Date and time widgets in a custom form need the admin JS and `admin:jsi18n`. See [actions.md](actions.md#action-with-an-intermediate-form-page-detail-action).

## ArrayWidget and WysiwygWidget (`unfold.contrib.forms`)

These need `"unfold.contrib.forms"` in `INSTALLED_APPS`.

```python
from django.contrib.postgres.fields import ArrayField
from django.db import models
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget

class ArticleAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},   # Trix editor; no file upload
        ArrayField: {"widget": ArrayWidget},
    }
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["tags"].widget = ArrayWidget(choices=TagChoices)  # choices -> select per item
        return form
```

- `ArrayWidget` does **not** read choices from the model field. Pass `choices=` explicitly, usually in `get_form`.
- `WysiwygWidget` is the [Trix](https://trix-editor.org/) editor. To include images, insert URLs of files you uploaded elsewhere.

## Autocomplete form fields (custom forms)

`unfold.fields.UnfoldAdminAutocompleteModelChoiceField` and `UnfoldAdminMultipleAutocompleteModelChoiceField` are backed by a JSON view.

```python
from unfold.fields import UnfoldAdminAutocompleteModelChoiceField, UnfoldAdminMultipleAutocompleteModelChoiceField
from unfold.views import BaseAutocompleteView

class ProductAutocompleteView(BaseAutocompleteView):   # ListView; returns {"results": [{id, text}], "pagination": {"more"}}
    model = Product
    def dispatch(self, request, *args, **kwargs):
        # permission checks here
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        term = self.request.GET.get("term")             # search text
        qs = super().get_queryset()
        return qs.filter(name__icontains=term) if term else qs

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    custom_urls = (("autocomplete", "product_autocomplete", ProductAutocompleteView.as_view()),)

class PickForm(forms.Form):
    product = UnfoldAdminAutocompleteModelChoiceField(
        queryset=Product.objects.all(),                 # used for validation; must match the view
        url_path="admin:product_autocomplete",
    )
    products = UnfoldAdminMultipleAutocompleteModelChoiceField(
        queryset=Product.objects.all(), url_path="admin:product_autocomplete")
```

The full queryset is evaluated on render, which is slow for big tables. Narrow it in the **form's** `__init__`:
- **GET:** set the queryset to `none()`, or to `filter(pk__in=initial)` when there are initial values.
- **POST:** set it to `filter(pk__in=request.POST.getlist("field"))`.

You must pass `request` into the form yourself, for example through `get_form_kwargs`. The docs show this snippet on the view class by mistake. It belongs on the form.

## Crispy Forms (`unfold_crispy` template pack)

```python
INSTALLED_APPS = ["unfold", ..., "crispy_forms"]
CRISPY_TEMPLATE_PACK = "unfold_crispy"              # skip if the front end uses another pack
CRISPY_ALLOWED_TEMPLATE_PACKS = ["unfold_crispy"]
```

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("field1", "field2")

class CrispyView(UnfoldModelAdminViewMixin, FormView):  # register as a custom page
    title = "Custom title"
    form_class = CustomForm
    success_url = reverse_lazy("admin:index")
    permission_required = ("app.change_model",)
    template_name = "app/crispy.html"
```

```django
{% extends "admin/base.html" %}
{% load crispy_forms_tags %}
{% block extrahead %}{{ block.super }}<script src="{% url 'admin:jsi18n' %}"></script>{{ form.media }}{% endblock %}
{% block content %}{% crispy form "unfold_crispy" %}{% endblock %}
```

Formsets work as follows:
- Use a `FormHelper` with `template = "unfold_crispy/layout/table_inline_formset.html"`, a unique `form_id` (required for dynamic rows) and `form_add = True`.
- Add submit buttons with `self.add_input(Submit(...))`, importing `Submit` from `unfold.layout`.
- Build the form class with `modelformset_factory(..., extra=1, can_delete=True)` in `get_form_class`.
- Render with `{% crispy form helper "unfold_crispy" %}`.
- Row deletion and min/max form counts are supported (v0.99.0+).

`unfold.layout` also exports `Button`, `FieldsetSubheader` and `Hr` (from source; undocumented).

## JSONSchemaField

New in v0.108.0. **Not in the docs snapshot.** Verified against the v0.110.0 source and tests.

```python
from unfold.models.fields import JSONSchemaField

class Profile(models.Model):
    data = JSONSchemaField(schema={"type": "object", "properties": {"name": {"type": "string"}}},
                           null=True, blank=True)   # schema may be a dotted path to a callable returning a dict
```

- The field renders a schema-driven editor (Jedison, `UnfoldAdminJSONSchemaWidget`).
- Model validation runs `jsonschema` when it is installed (`django-unfold[jsonschema]`); otherwise validation is skipped silently.
- The form field is `unfold.fields.UnfoldAdminJSONSchemaField(schema=...)`.
- Check the live docs before relying on details.
