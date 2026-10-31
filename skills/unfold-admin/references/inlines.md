# Inlines

Docs: [introduction](https://unfoldadmin.com/docs/inlines/introduction/) · [options](https://unfoldadmin.com/docs/inlines/options/) · [sortable](https://unfoldadmin.com/docs/inlines/sortable/) · [paginated](https://unfoldadmin.com/docs/inlines/paginated/) · [nested](https://unfoldadmin.com/docs/inlines/nested/) · [nonrelated](https://unfoldadmin.com/docs/inlines/nonrelated/) · [inline tabs](https://unfoldadmin.com/docs/tabs/inline/)

## Classes

| Class | Import from |
|---|---|
| `StackedInline`, `TabularInline` | `unfold.admin` |
| `GenericStackedInline`, `GenericTabularInline` | `unfold.admin` |
| `NonrelatedStackedInline`, `NonrelatedTabularInline` | `unfold.contrib.inlines.admin` (needs `"unfold.contrib.inlines"` in `INSTALLED_APPS`) |

Django's own inline classes work but render unstyled. Always use the Unfold ones.

## Options

| Attribute or method | Default | Effect |
|---|---|---|
| `tab = True` | `False` | Puts the inline in the changeform tab navigation |
| `per_page = 10` | `None` | Paginates the inline. Each inline gets its own query parameter. Not AJAX, so the page reloads. Controls are hidden on a single page. Give the model an ordering |
| `collapsible = True` | `False` | StackedInline only. Rows start collapsed; rows with errors open |
| `show_count = True` | `False` | Count badge. Runs `count()` per inline, so avoid on big querysets |
| `get_count(self, request, obj)` | – | Custom badge text |
| `get_count_variant(self, request, obj)` | – | `primary danger success info warning` |
| `show_title = False` | `True` | Hides the row title. **StackedInline also needs `can_delete = False`** |
| `ordering_field` / `hide_ordering_field` | – | Drag-and-drop sorting (below) |
| `inlines = [...]` | – | Nested inlines (below) |
| Model method `get_inline_title(self)` | – | Row title in inlines instead of `__str__` |

**Breaking change in v0.104.0:** `hide_title` was renamed to `show_title`, with the meaning inverted.

```python
from unfold.admin import ModelAdmin, StackedInline, TabularInline

class ItemInline(TabularInline):
    model = Item
    tab = True
    per_page = 10
    show_count = True
    ordering_field = "weight"
    hide_ordering_field = True

class NoteInline(StackedInline):
    model = Note
    collapsible = True

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [ItemInline, NoteInline]
```

## Sortable inlines

- The ordering field must be `models.PositiveIntegerField(default=0, db_index=True)`.
- New rows must be saved before they can be dragged.
- The docs example also sets `list_display = [..., "weight"]` on the inline. Django inlines do not use `list_display`, so treat the docs' "weight is mandatory field" note as meaning the ordering field must be a real model field.

## Nested inlines

```python
class SubTaskInline(TabularInline):
    model = SubTask

class TaskInline(TabularInline):     # Stacked and Tabular can be mixed
    model = Task
    inlines = [SubTaskInline]        # a third level is NOT supported

class ProjectAdmin(ModelAdmin):
    inlines = [TaskInline]
```

Limits: one nested level only, and no nesting through M2M.

## Nonrelated inlines (no FK to the parent)

```python
from unfold.contrib.inlines.admin import NonrelatedTabularInline

class OtherInline(NonrelatedTabularInline):
    model = OtherModel
    fields = ["field1", "field2"]          # omit to show all
    def get_form_queryset(self, obj):      # required
        return self.model.objects.filter(owner=obj.owner)
    def save_new_instance(self, parent, instance):   # required
        instance.owner = parent.owner
```

This is based on django-nonrelated-inlines.
