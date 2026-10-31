# Third-party integrations

Docs: [integrations](https://unfoldadmin.com/docs/integrations/), plus one page per package, linked below.

General rule: if a package registers its own admin classes, **unregister them and re-register** with `unfold.admin.ModelAdmin` mixed in. Otherwise those pages stay unstyled.

## Summary

| Package | `INSTALLED_APPS` | Admin change | Doc |
|---|---|---|---|
| django-import-export | `unfold.contrib.import_export` | Set the form classes (below) | [link](https://unfoldadmin.com/docs/integrations/django-import-export/) |
| django-simple-history | `unfold.contrib.simple_history`, after `unfold` and **before** `simple_history` | `class X(SimpleHistoryAdmin, ModelAdmin)` | [link](https://unfoldadmin.com/docs/integrations/django-simple-history/) |
| django-guardian | `unfold.contrib.guardian` | None; adds an "Object permissions" button on the changeform | [link](https://unfoldadmin.com/docs/integrations/django-guardian/) |
| django-constance | `unfold.contrib.constance`, **before** `constance` | `CONSTANCE_ADDITIONAL_FIELDS` (below) | [link](https://unfoldadmin.com/docs/integrations/django-constance/) |
| django-location-field | `unfold.contrib.location_field`, **before** `location_field` | Widget override (below) | [link](https://unfoldadmin.com/docs/integrations/django-location-field/) |
| django-hijack | `unfold.contrib.hijack` | None | [link](https://unfoldadmin.com/docs/integrations/django-hijack/) |
| django-celery-beat | none | Re-register all five admins (below) | [link](https://unfoldadmin.com/docs/integrations/django-celery-beat/) |
| django-waffle | none | Re-register; use Unfold's `FlagAdmin` (below) | [link](https://unfoldadmin.com/docs/integrations/django-waffle/) |
| django-money | none | None; `MoneyField` gets `UnfoldAdminMoneyWidget` automatically | [link](https://unfoldadmin.com/docs/integrations/django-money/) |
| django-json-widget | none | None; styled by CSS | [link](https://unfoldadmin.com/docs/integrations/django-json-widget/) |
| djangoql | none | None; the search UI is styled and the help link hidden | [link](https://unfoldadmin.com/docs/integrations/djangoql/) |
| django-reversion | `unfold.contrib.reversion` | **Live page not accessible**; see below | [link](https://unfoldadmin.com/docs/integrations/django-reversion/) |
| django-reversion-compare | `unfold.contrib.reversion_compare` | **Live page not accessible**; see below | [link](https://unfoldadmin.com/docs/integrations/django-reversion-compare/) |
| django-modeltranslation | none | **Deprecated in v0.102.0; no code left in v0.110.0** | [link](https://unfoldadmin.com/docs/integrations/django-modeltranslation/) |

## django-import-export

```python
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

class ExampleAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm          # or SelectableFieldsExportForm
```

`unfold.contrib.import_export.admin.ExportActionModelAdmin` was needed only before import-export 4.x and **no longer exists in Unfold v0.110.0**. With import-export 4.x, use `import_export.admin.ExportActionModelAdmin` directly.

## django-constance

```python
from unfold.contrib.constance.settings import UNFOLD_CONSTANCE_ADDITIONAL_FIELDS

CONSTANCE_ADDITIONAL_FIELDS = {
    **UNFOLD_CONSTANCE_ADDITIONAL_FIELDS,   # Unfold widgets for standard types plus image_field and file_field
    "choice_field": ["django.forms.fields.ChoiceField",
                     {"widget": "unfold.widgets.UnfoldAdminSelectWidget",
                      "choices": (("light-blue", "Light blue"), ("dark-blue", "Dark blue"))}],
}
```

Datetime, date and time support was added in v0.106.0.

## django-location-field

```python
from unfold.widgets import UnfoldAdminLocationWidget

class PlaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["location"].widget = UnfoldAdminLocationWidget()   # base_fields=["city"], zoom=7

@admin.register(Place)
class PlaceAdmin(ModelAdmin):
    form = PlaceForm
```

## django-celery-beat

```python
from django_celery_beat.admin import (ClockedScheduleAdmin as BaseClockedScheduleAdmin,
    CrontabScheduleAdmin as BaseCrontabScheduleAdmin, PeriodicTaskAdmin as BasePeriodicTaskAdmin,
    PeriodicTaskForm, TaskSelectWidget)
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask, SolarSchedule
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

for m in (PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule):
    admin.site.unregister(m)

class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass

class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()

@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm

@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin): pass

@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin): pass

@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin): pass

@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin): pass
```

## django-waffle

```python
from waffle.admin import SampleAdmin as BaseSampleAdmin, SwitchAdmin as BaseSwitchAdmin
from waffle.models import Flag, Sample, Switch
from unfold.contrib.waffle.admin import FlagAdmin as BaseFlagAdmin   # replaces users field with autocomplete

for m in (Flag, Switch, Sample):
    admin.site.unregister(m)

@admin.register(Flag)
class FlagAdmin(BaseFlagAdmin): pass          # already Unfold-based

@admin.register(Switch)
class SwitchAdmin(ModelAdmin, BaseSwitchAdmin): pass

@admin.register(Sample)
class SampleAdmin(ModelAdmin, BaseSampleAdmin): pass
```

## Limitations to mention

- **hijack:** outside the admin, the impersonation banner may render unstyled.
- **djangoql:** its own extra pages, such as the syntax help, are not styled.
- **guardian:** see the official guardian docs for its own setup.

## django-reversion and django-reversion-compare (v0.109.0+)

The live integration pages exist (they are linked from the Unfold README) but were not accessible when this skill was built. They are not in the docs snapshot. What the source and test project show:
- The apps are `unfold.contrib.reversion` and `unfold.contrib.reversion_compare`. The test project lists them before `reversion` and `reversion_compare`.
- They override those packages' history and compare templates.

Read the live pages before adding admin mixins.

## django-modeltranslation (deprecated)

- The docs page describes `class X(ModelAdmin, TabbedTranslationAdmin)` and `UNFOLD["EXTENSIONS"]["modeltranslation"]["flags"]`.
- The feature was deprecated in v0.102.0, and v0.110.0 contains no modeltranslation code.
- **Do not add it to new code.** If a project already uses it, tell the user that Unfold no longer supports it.
