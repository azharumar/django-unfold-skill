# List filters

Docs: [introduction](https://unfoldadmin.com/docs/filters/introduction/) · [text](https://unfoldadmin.com/docs/filters/text/) · [dropdown](https://unfoldadmin.com/docs/filters/dropdown/) · [checkbox & radio](https://unfoldadmin.com/docs/filters/checkbox-radio/) · [numeric](https://unfoldadmin.com/docs/filters/numeric/) · [datetime](https://unfoldadmin.com/docs/filters/datetime/) · [autocomplete](https://unfoldadmin.com/docs/filters/autocomplete/) · [horizontal](https://unfoldadmin.com/docs/filters/horizontal/)

## Prerequisites

- Add `"unfold.contrib.filters"` to `INSTALLED_APPS`, straight after `"unfold"`.
- Import every class from `unfold.contrib.filters.admin`.
- Set `list_filter_submit = True` for any input-based filter (text, numeric, date, autocomplete). Without it there is no way to submit.
- Field filters are written as `("field", FilterClass)` tuples. Custom filters are bare classes.

## Choosing a filter

| Need | Class | Field type |
|---|---|---|
| Free-text `icontains` on one field | `FieldTextFilter` | Char and text |
| Custom text query | subclass `TextFilter` | any |
| Select from field choices | `ChoicesDropdownFilter` / `MultipleChoicesDropdownFilter` | field with `choices` |
| Select a related object | `RelatedDropdownFilter` / `MultipleRelatedDropdownFilter` | FK and M2M (small tables only) |
| Custom select | subclass `DropdownFilter` / `MultipleDropdownFilter` | any |
| Large related table with search | `AutocompleteSelectFilter` / `AutocompleteSelectMultipleFilter` | FK and M2M; the target admin needs `search_fields` |
| All choices visible | `ChoicesRadioFilter` (adds "All") / `ChoicesCheckboxFilter` | field with `choices` |
| Boolean Yes/No/All | `BooleanRadioFilter` | `BooleanField` |
| Related objects as checkboxes | `RelatedCheckboxFilter` | FK |
| Distinct column values as checkboxes | `AllValuesCheckboxFilter` | any |
| Custom radio or checkbox | subclass `RadioFilter` / `CheckboxFilter` | any |
| `>=` one number | `SingleNumericFilter` | numeric |
| Number range (`gte`/`lte`) | `RangeNumericFilter` | numeric |
| Range slider | `SliderNumericFilter` (`MAX_DECIMALS`, `STEP`) | numeric |
| Range on an annotation | subclass `RangeNumericListFilter` (`parameter_name`, `title`) | not tied to a field |
| Date range | `RangeDateFilter` | `DateField` |
| Datetime range | `RangeDateTimeFilter` | `DateTimeField` |

- Dropdowns use Select2. There is no native `<select>` option.
- Dropdown filters have no autocomplete, so use the autocomplete filters for big tables.

## Example

```python
from django.core.validators import EMPTY_VALUES
from django.db.models import Count
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    AutocompleteSelectMultipleFilter, BooleanRadioFilter, ChoicesCheckboxFilter,
    FieldTextFilter, RangeDateTimeFilter, RangeNumericFilter, RangeNumericListFilter,
    RelatedDropdownFilter, SliderNumericFilter, TextFilter,
)

class CodeFilter(TextFilter):           # same pattern for DropdownFilter / RadioFilter / CheckboxFilter
    title = _("Code")
    parameter_name = "code"
    # DropdownFilter/RadioFilter/CheckboxFilter also define lookups(self, request, model_admin)
    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(code__startswith=self.value())
        return queryset

class StepSlider(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 10

class ItemsCountFilter(RangeNumericListFilter):
    parameter_name = "items_count"      # must match an annotation
    title = "items"

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_filter_submit = True
    list_filter = [
        CodeFilter,
        ("name", FieldTextFilter),
        ("status", ChoicesCheckboxFilter),
        ("is_paid", BooleanRadioFilter),
        ("customer", RelatedDropdownFilter),
        ("tags", AutocompleteSelectMultipleFilter),   # TagAdmin must define search_fields
        ("total", RangeNumericFilter),
        ("weight", StepSlider),
        ("created_at", RangeDateTimeFilter),
        ItemsCountFilter,
    ]
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(items_count=Count("item", distinct=True))
```

## Layout options

```python
list_filter_options = {"category": {"label": _("Category"), "horizontal": True}}
list_filter_sheet = False      # sidebar instead of the default sheet
```

A filter class can also set `horizontal = True`, for example on a subclass of Django's `ChoicesFieldListFilter`.

## Errors in the docs examples (do not copy)

- In the dropdown example, `("fk", RelatedDropdownFilter)("fk_multi", ...)` is missing a comma between tuples.
- The numeric example calls `super().get_queryset()` without `request`.
- `EMPTY_VALUES` comes from `django.core.validators`.
