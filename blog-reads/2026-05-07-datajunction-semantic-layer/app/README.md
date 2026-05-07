# Semantic Layer Playground

Single-file demo. No build step.

```
open index.html        # macOS
xdg-open index.html    # Linux
```

What you can play with:

- **Pick a metric** (`dau` or `avg_session_minutes`).
- **Toggle dimensions** to slice by `country` or `plan_tier`.
- **Toggle filters** like `plan_tier = 'premium'`.
- **Change the time window** (7 / 30 / 90 days).

What you can watch:

- The **metric graph** highlights the path the planner walks for your request.
- The **generated SQL** regenerates instantly — same metric definition, different
  physical SQL depending on which dimensions you slice by.
- The **result preview** runs the same intent on a deterministic in-browser
  toy warehouse so the numbers move with your selections.
- The **definition pane** shows the YAML that a metric owner registers *once*
  in DJ; everything else is derived.

The whole thing is ~350 lines of vanilla JS in `index.html` — open it and read
the source alongside the deep-dive notes in [`../README.md`](../README.md).
