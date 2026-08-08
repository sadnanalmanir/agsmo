# Per-example diagrams (Mermaid)

Plain-text **Mermaid** sources — easier to maintain than hand-drawn SVG.

| File | Lesson |
|------|--------|
| [`01_minimal_goal.mmd`](01_minimal_goal.mmd) | Agent + one Goal |
| [`02_plan_with_constraints.mmd`](02_plan_with_constraints.mmd) | Plan + constraints + steps |
| [`03_action_and_explain.mmd`](03_action_and_explain.mmd) | Action / rationale / Outcome |
| [`04_literature_review_full.mmd`](04_literature_review_full.mmd) | Full happy path |
| [`05_failure_and_rollup.mmd`](05_failure_and_rollup.mmd) | Failure roll-up |

## How they render

The HTML tutorial loads [Mermaid.js](https://mermaid.js.org/) from a CDN and renders
the same definitions inline. Edit the `.mmd` files **and** the matching
`<div class="mermaid">` block in [`docs/tutorial.html`](../../docs/tutorial.html)
(keep them in sync), then push.

Preview a file on GitHub: open the `.mmd` in the GitHub UI (Mermaid often previews in markdown code blocks) or paste into https://mermaid.live/

## Why Mermaid not SVG

- Diff-friendly text in git  
- Layout handled by the renderer  
- One mental model for all lessons  
