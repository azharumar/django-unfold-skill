# ModelAdmin: changelist and changeform features

Covers: `unfold.admin.ModelAdmin` options, the `@display` decorator, conditional fields, fieldset tabs, sections (expandable rows), datasets, `InfinitePaginator`, sortable changelist, and readonly JSON.

Docs: [ModelAdmin options](https://unfoldadmin.com/docs/configuration/modeladmin/) · [@display](https://unfoldadmin.com/docs/decorators/display/) · [conditional fields](https://unfoldadmin.com/docs/configuration/conditional-fields/) · [fieldset tabs](https://unfoldadmin.com/docs/tabs/fieldsets/) · [sections](https://unfoldadmin.com/docs/configuration/sections/) · [datasets](https://unfoldadmin.com/docs/configuration/datasets/) · [paginator](https://unfoldadmin.com/docs/configuration/paginator/) · [sortable changelist](https://unfoldadmin.com/docs/configuration/sortable-changelist/) · [JSON field](https://unfoldadmin.com/docs/fields/json/)

## Option table (in addition to Django's)

| Attribute | Default | Effect |
|---|---|---|
| `show_add_link` | `True` | "Add" link in changelist and changeform |
| `warn_unsaved_form` | `False` | Warn before leaving a changeform with unsaved changes |
| `readonly_preprocess_fields` | `{}` | `{"field": "html.unescape" or callable}` applied before readonly render |
| `list_filter_submit` | `False` | Submit button in the filter panel (needed for input filters) |
| `list_filter_sheet` | `True` | `False` shows filters as a sidebar instead of a sheet |
| `list_filter_options` | `{}` | `{"field_path": {"label": ..., "horizontal": bool}}` |
| `list_fullwidth` | `False` | Full-width changelist |
| `list_disable_select_all` | `False` | Hide "select all" |
| `list_sections` | – | Expandable row sections (below) |
| `actions_list` / `actions_row` / `actions_detail` / `actions_submit_line` | – | See [actions.md](actions.md) |
| `actions_list_hide_default` / `actions_detail_hide_default` | `False` | Hide built-in and third-party actions |
| `change_form_before_template` / `change_form_after_template` | `None` | Template included inside the form |
| `change_form_outer_before_template` / `change_form_outer_after_template` | `None` | Template included outside the form |
| `change_form_show_cancel_button` | `False` | Cancel button in the submit line |
| `change_form_datasets` | – | Embedded changelists (below) |
| `conditional_fields` | – | Show or hide fields (below) |
| `ordering_field`, `hide_ordering_field` | `None`, `False` | Drag-and-drop sorting (below) |
| `custom_urls` | `()` | `((path, name, view), ...)`, mounted under this model's admin URL and named `admin:<name>` |
| `paginator` | Django default | `unfold.paginator.InfinitePaginator` for huge tables |

`list_before_template` and `list_after_template` also exist in the v0.110.0 source and changelist template. They are not in the docs snapshot.

Apply Unfold widgets to every field of a type with `formfield_overrides`. See [forms-and-widgets.md](forms-and-widgets.md).

## `@display` (`unfold.decorators.display`)

A drop-in replacement for Django's `display`. It keeps `description`, `ordering`, `boolean`, `empty_value` and so on, and adds `label`, `header`, `dropdown` and `formatting`.

```python
from unfold.decorators import display

class OrderAdmin(ModelAdmin):
    list_display = ["customer", "status_badge", "status_named", "price"]

    @display(description=_("Status"), ordering="status",
             label={Status.ACTIVE: "success", Status.PENDING: "info",
                    Status.INACTIVE: "warning", Status.CANCELLED: "danger"})
    def status_badge(self, obj):
        return obj.status                         # label=True -> default colour

    @display(description=_("Status"), label=True)
    def status_named(self, obj):
        return obj.status, obj.get_status_display()   # (key used for colour, text shown)

    @display(header=True)
    def customer(self, obj):
        return [obj.name, obj.email, "AB",        # line 1, line 2 (or None), initials
                {"path": obj.photo_url, "squared": True, "borderless": True,
                 "width": 64, "height": 48}]      # optional image; replaces initials

    @display(description=_("Price"), formatting="price")   # right-aligned price
    def price(self, obj):
        return obj.total
```

Dropdown cell (`dropdown=True`). Return either a list or raw content:

```python
@display(description=_("Items"), dropdown=True)
def items(self, obj):
    return {"title": "3 items",                # trigger text (required)
            "items": [{"title": "A", "link": "#"}],   # or "content": render_to_string(...)
            "striped": True, "height": 200, "max_height": 300, "width": 240}
```

## Conditional fields

Show or hide changeform fields live with an Alpine.js expression over other field names.

```python
class UserAdmin(ModelAdmin):
    conditional_fields = {
        "country": "different_address == true",
        "city": "different_address == true",
    }
```

- For multi-widget fields such as `SplitDateTimeField`, refer to `name_0` and `name_1`.
- MultiWidget support was fixed in v0.108.0.
- The docs example leaves out the commas between dict entries. Include them.

## Fieldset tabs

Add `"classes": ["tab"]` to fieldsets that have a title. They render as one tabbed block inside the form, not at the page top. Fieldsets without a title are left out of the tabs.

```python
fieldsets = (
    (None, {"fields": ["name"]}),
    (_("Address"), {"classes": ["tab"], "fields": ["city", "street"]}),
    (_("Billing"), {"classes": ["tab"], "fields": ["iban"]}),
)
```

## Sections: expandable changelist rows

```python
from unfold.sections import TableSection, TemplateSection

class ItemsSection(TableSection):
    verbose_name = _("Items")        # title above the table
    height = 300                     # fixed height, scrolls
    related_name = "item_set"        # reverse relation on the row object
    fields = ["pk", "title", "custom_field"]
    def custom_field(self, instance):
        return instance.pk

class CardSection(TemplateSection):
    template_name = "app/section.html"

class OrderAdmin(ModelAdmin):
    list_sections = [CardSection, ItemsSection]   # several TableSections are allowed
    list_per_page = 20
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("item_set")
```

`TableSection` adds a query per row. Always `prefetch_related` the relation. A lower `list_per_page` is only a stop-gap.

## Datasets: a changelist inside a changeform

```python
from unfold.datasets import BaseDataset

class ItemDatasetAdmin(ModelAdmin):          # NOT registered with @admin.register
    search_fields = ["name"]
    list_display = ["name", "city"]
    list_display_links = ["name"]
    list_per_page = 20                       # default 10
    actions = ["custom_action"]
    def get_queryset(self, request):
        obj_id = self.extra_context.get("object")   # parent pk; None on the add page
        if not obj_id:
            return super().get_queryset(request).none()
        return super().get_queryset(request).filter(parent__pk=obj_id)  # + permission filtering

class ItemDataset(BaseDataset):
    model = Item
    model_admin = ItemDatasetAdmin
    tab = True                               # show as a tab

class ParentAdmin(ModelAdmin):
    change_form_datasets = [ItemDataset]
```

- Supported: `list_display`, links, search, pagination and actions.
- **Not supported:** `list_filter` and sorting.
- Permissions and parent scoping are your job, in `get_queryset`.

## InfinitePaginator

For very large tables. It skips `COUNT`, shows only previous and next, and has no last page.

```python
from unfold.paginator import InfinitePaginator

class LogAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
```

## Sortable changelist (drag and drop)

```python
class Item(models.Model):
    weight = models.PositiveIntegerField(_("weight"), default=0, db_index=True)
    class Meta:
        ordering = ["weight"]

class ItemAdmin(ModelAdmin):
    ordering_field = "weight"
    hide_ordering_field = True
```

- The field must be a `PositiveIntegerField(db_index=True)`, and the model must be ordered by it.
- Reordering works only within the current page. Save before changing page.
- The sortable-inlines page says sorting is "not available in the changelist". That page predates the sortable-changelist feature and is superseded.

## Readonly JSON

- A `JSONField` listed in `readonly_fields` is pretty-printed.
- With Pygments installed (`pip install pygments`, or the `django-unfold[pygments]` extra), it is also syntax-highlighted.
- An editable `JSONField` renders as a plain `UnfoldAdminTextareaWidget`.
- To format without Pygments, store the value pre-indented with a custom encoder: `json.JSONEncoder` with `indent=4, sort_keys=True`, set as the field's `encoder`.

For schema-driven JSON editing (v0.108.0+, not in the docs snapshot), see [forms-and-widgets.md](forms-and-widgets.md#jsonschemafield).
