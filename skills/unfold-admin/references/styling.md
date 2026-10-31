# Theming, colours, custom CSS and JS, Tailwind

Docs: [settings](https://unfoldadmin.com/docs/configuration/settings/) · [loading files](https://unfoldadmin.com/docs/styles-scripts/loading-files/) · [customizing Tailwind](https://unfoldadmin.com/docs/styles-scripts/customizing-tailwind/) · [development](https://unfoldadmin.com/docs/development/)

## Theme settings

```python
UNFOLD = {
    "THEME": "dark",            # or "light": forces the theme and removes the switcher; omit for user choice
    "BORDER_RADIUS": "6px",
    "COLORS": {
        # shades 50, 100 ... 900, 950; any subset is deep-merged with the defaults
        "primary": {"500": "oklch(62.7% .265 303.9)", "600": "oklch(55.8% .288 302.321)"},
        "base": {"950": "oklch(13% .028 261.692)"},
        "font": {
            "subtle-light": "var(--color-base-500)",    "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",   "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)", "important-dark": "var(--color-base-100)",
        },
    },
}
```

- `base` and `primary` take the shades `50, 100, 200, ... 900, 950`.
- Values are CSS colours. Current Unfold defaults use `oklch(...)`.
- `UNFOLD` is deep-merged with the defaults (verified in v0.110.0 `settings.get_config`). To rebrand, overriding `primary` is enough.
- Each colour is exposed as a CSS variable, `--color-<group>-<shade>`, e.g. `var(--color-primary-700)`. Use these in your CSS and chart datasets.
- Tailwind utility names in Unfold templates follow the same tokens: `bg-primary-600`, `text-base-500`, `dark:...`, `rounded-default`, `text-important`, `text-subtle`.

## Loading your own CSS and JS (all admin pages)

```python
from django.templatetags.static import static

UNFOLD = {
    "STYLES": [lambda request: static("css/admin.css")],
    "SCRIPTS": [lambda request: static("js/admin.js")],
}
```

Run `collectstatic` in production.

## Custom Tailwind classes

Unfold's CSS contains only the classes Unfold's own templates use. **New Tailwind classes in your templates do nothing until you compile them.** Choose one of these:

1. **Plain CSS, loaded through `STYLES`.** The docs recommend this for v0.56+.
2. **Tailwind 4, for Unfold 0.57+:**

```bash
npm i tailwindcss @tailwindcss/cli
```

```css
/* styles.css */
@import 'tailwindcss';
```

```bash
npx @tailwindcss/cli -i styles.css -o your_project/static/css/styles.css --minify
```

Then add the output file to `STYLES`.

Tailwind 3 with a `tailwind.config.js` that maps `rgb(var(--color-*) / <alpha-value>)` applies only to Unfold below 0.56. **Do not use it with current Unfold**, where colours are `oklch` values rather than RGB triplets.

## Changing Unfold itself (contributors)

- Compile Unfold's CSS with `tailwindcss -i src/unfold/styles.css -o src/unfold/static/unfold/css/styles.css --minify --watch`.
- Elements created by jQuery cannot take template classes, so they are styled with `@apply` in `styles.css`. This covers date pickers, calendars and selectors.
- Run the test server with `cd tests/server && uv run -- python manage.py runserver`, then `uv run -- python manage.py createsuperuser`.
- Run tests with `uv run -- pytest .` from the repo root.
- Set up pre-commit with `pre-commit install` and `pre-commit install --hook-type commit-msg`.
