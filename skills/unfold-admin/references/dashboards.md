# Dashboard and components

Docs: [dashboard](https://unfoldadmin.com/docs/configuration/dashboard/) · [components intro](https://unfoldadmin.com/docs/components/introduction/) · [component class](https://unfoldadmin.com/docs/components/component-class/) · [button](https://unfoldadmin.com/docs/components/button/) · [card](https://unfoldadmin.com/docs/components/card/) · [chart](https://unfoldadmin.com/docs/components/chart/) · [cohort](https://unfoldadmin.com/docs/components/cohort/) · [layer](https://unfoldadmin.com/docs/components/layer/) · [link](https://unfoldadmin.com/docs/components/link/) · [progress](https://unfoldadmin.com/docs/components/progress/) · [table](https://unfoldadmin.com/docs/components/table/) · [tracker](https://unfoldadmin.com/docs/components/tracker/)

## Custom dashboard

1. Make sure `TEMPLATES[0]["DIRS"]` includes `BASE_DIR / "templates"`.
2. Create `templates/admin/index.html`:

```django
{% extends "admin/base.html" %}
{% load i18n unfold %}
{% block title %}{% if subtitle %}{{ subtitle }} | {% endif %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock %}
{% block branding %}{% include "unfold/helpers/site_branding.html" %}{% endblock %}
{% block content %}
  {# components here #}
{% endblock %}
```

3. Pass data in with `UNFOLD["DASHBOARD_CALLBACK"] = "app.views.dashboard_callback"`:

```python
def dashboard_callback(request, context):
    context.update({"kpis": [...], "chart_data": json.dumps({...})})
    return context
```

**Tailwind classes you write yourself are not compiled.** Unfold ships only the classes it uses. Write plain CSS, or build a Tailwind stylesheet and load it with `STYLES`. See [styling.md](styling.md).

## Component tag

```django
{% load unfold %}
{% component "unfold/components/card.html" with title=t class="lg:w-1/3" %}
  {% component "unfold/components/title.html" %}{{ metric }}{% endcomponent %}
{% endcomponent %}
```

- Nested content arrives as `children`. Pass parameters with `with k=v`.
- `{% capture as var %}...{% endcapture %}` stores rendered HTML for parameters such as `action`. Add `silent` to suppress output.
- Use `{% trans "..." as var %}` for translated parameters.

## Component templates and parameters

| Template | Parameters |
|---|---|
| `unfold/components/button.html` | `variant` (`default secondary danger ghost`), `size` (`sm md`), `href` (renders as a link), `submit`, `name`, `value`, `form`, `title`, `attrs` (dict), `extra_attrs` (str), `class` |
| `unfold/components/card.html` | `title`, `label` (floating, top right), `action` (HTML beside title), `icon` (background icon, for KPI cards), `footer`, `href` (clickable card), `disable_border`, `class`, `title_class` |
| `unfold/components/chart/bar.html`, `.../chart/line.html` | `data` (JSON string), `options` (JSON string), `height`, `width`, `class`, `responsive` (default true), `tooltip` (default true) |
| `unfold/components/chart/cohort.html` | `data` |
| `unfold/components/tracker.html` | `data`, `class` (and `size`: `md`/`sm`) |
| `unfold/components/table.html` | `table`, `title`, `striped`, `card_included`, `height` |
| `unfold/components/progress.html` | `value`, `title`, `description`, `class`, or `items` for segments |
| `unfold/components/link.html` | `href`, `icon`, `external` (new tab and icon), `class` |
| `unfold/components/navigation.html` | `items`, `class` |
| `unfold/components/container.html`, `flex.html` (`col`), `icon.html`, `separator.html`, `text.html`, `title.html` | `class` |
| `unfold/components/layer.html` | none; a wrapper that exposes `component_class` context to children |

- The components intro table lists `unfold/components/cohort.html`. The real path is `unfold/components/chart/cohort.html`.
- **v0.106.0 card additions** (from source, not in the docs snapshot): `title_icon` and `description`.

## Component classes: Python data preparation

```python
from unfold.components import BaseComponent, register_component

@register_component
class SalesChart(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"height": 320, "data": json.dumps({
            "labels": ["Mon", "Tue", "Wed"],
            "datasets": [
                {"label": "Orders", "data": [12, 19, 3], "backgroundColor": "var(--color-primary-700)"},
                {"label": "Trend", "data": [3, 12, 5], "borderColor": "var(--color-primary-400)",
                 "type": "line", "displayYAxis": True, "maxTicksXLimit": 50, "suffixYAxis": "€"},
            ]})})
        return context
```

```django
{% component "unfold/components/card.html" with title="Sales" %}
  {% component "unfold/components/chart/bar.html" with component_class="SalesChart" %}{% endcomponent %}
{% endcomponent %}
```

- Reference the class by name in `component_class`.
- The module must be imported at start-up, for example in `admin.py`.
- Use a component class or a `DASHBOARD_CALLBACK` variable for data; either works.

## Data shapes

**Chart** (Chart.js):
- `data` takes `labels` and `datasets`.
- Dataset extras: `displayYAxis`, `displayXAxis`, `maxTicksXLimit` and `suffixYAxis`.
- `options` takes Chart.js options as JSON. JavaScript functions are not supported.

**Table:**

```python
{"collapsible": True, "headers": ["A", {"content": "B", "class": "text-right"}],
 "rows": [["a", "b"],
          {"cols": ["c", "d"], "attrs": {"data-x": "1"},
           "table": {"collapsible": True, "headers": [...], "rows": [[...]]}}]}   # nested table
```

**Cohort:**

```python
{"headers": [{"title": "Week 1", "subtitle": "opt"}],
 "rows": [{"header": {"title": "Jan", "subtitle": "opt"}, "cols": [{"value": "1", "subtitle": "opt"}]}]}
```

**Tracker:** a list of cells. Every key is optional.

```python
[{"color": "bg-primary-400 dark:bg-primary-700", "tooltip": "3 events", "href": "...", "class": "x"}]
```

**Progress:**
- Single bar: `{"title", "description", "value": 57.5, "progress_class"}`.
- Segmented: `{"title", "description", "items": [{"title", "value": 30.0, "progress_class": "..."}]}`.
- The docs write the segment key as `progress-class`, but the v0.110.0 template reads `item.progress_class`.

## Docs example errors (do not copy)

- The button `attrs` example is missing a `{`.
- The tracker `context.update` is missing a comma.
- The chart examples omit the `register_component` import.
