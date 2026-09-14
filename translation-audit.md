# Translation audit: Altair → ggplot2 (spec 9)

**Source spec (Altair, spec 9 in `specs_altair.py`):**
```python
alt.Chart(df).mark_bar().encode(
    x=alt.X("hours:Q", bin=alt.Bin(step=2)),
    y=alt.Y("count()", stack="zero"),
    color=alt.Color("mean(lines):Q", scale=alt.Scale(scheme="blues"))
)
```
Chosen as the "most complex" spec because it stacks four grammar components on
top of the histogram parent: a bin statistic, a count aggregate, a position
adjustment, and a second aggregate (`mean(lines)`) mapped through a continuous
color scale. Rendered as `out/09.png`.

**Raw translation** (unmodified LLM output): `translated_spec9.R`

**Run:** executed via `run_translated_spec9.R` (identical logic, with data
loading and a `ggsave` call added so it produces a comparable PNG) against
`pr_data.csv` — the exact same synthetic dataset used for the Altair specs,
exported so both languages plot identical numbers. Output: `spec9_ggplot2.png`.

## Divergence table

| Component | Source (Altair) behavior | Translated (ggplot2) behavior | Visible consequence |
|---|---|---|---|
| Binning + cross-variable aggregation | Vega-Lite bins `hours` and aggregates `mean(lines)` *within the same declarative encoding block* — one spec, no separate data step | ggplot2/`geom_col` has no way to bin one variable and aggregate a *different* variable into fill inside the plot call; the translation silently introduces a `dplyr` pre-aggregation step (`floor(hours/2)*2`, `group_by`, `summarise`) that lives outside the grammar entirely | The two charts can still end up looking identical, but the ggplot2 "spec" is no longer self-contained — the binning logic (and its edge convention) now lives in ordinary data-wrangling code the grammar can't check or reason about |
| Bin edge convention | Vega-Lite's `bin: {step: 2}` anchors bins at multiples of the step starting from a computed origin near the data minimum, with left-closed/right-open intervals | The translation's `floor(hours/2)*2` anchors bins at multiples of 2 starting at 0, also left-closed/right-open | For this dataset the two conventions happen to agree closely (values are far from 0), but they are not guaranteed to agree in general — a translator that trusts this pattern on a variable with a non-zero-friendly range would get silently shifted bin edges |
| Position ("stack") on a continuous-fill bar | `stack="zero"` is declared, but since `color` is a per-bin aggregate (one value per x-bin), there is only one mark per bin — stacking has no visible effect | `geom_col()`'s default position is also `"stack"`, and since the data was pre-aggregated to one row per bin, stacking likewise has no visible effect | **No divergence** — worth stating explicitly, since a translation that happens to match should be shown to match, not just assumed |
| Continuous color scale, direction and stops | The source spec pins the scale to Altair's `"blues"` scheme, which runs **light-at-low → dark-at-high** (confirmed by rendering `out/09.png`) | The translation hard-codes `scale_fill_gradient(low = "#132B43", high = "#56B1F7")` — ggplot2's own default continuous gradient, which runs **dark-at-low → light-at-high**, and uses different hex stops than Vega-Lite's `"blues"` scheme | Comparing `out/09.png` to `spec9_ggplot2.png` directly: the same underlying values are encoded with opposite light/dark polarity and a visibly different shade of blue. A translator asked to reproduce a named scheme (`"blues"`) reached for the target library's own default blue rather than the source library's actual color stops for that name |

## Summary
Three of the four audited components diverge in ways that produce a visibly
different figure from identical data (aggregation location, bin-edge
anchoring, and color-scale direction/stops); one component (stacking) matches
exactly and is reported as matching rather than omitted. The recurring pattern
is that Altair's single declarative encoding block does work — binning a
different variable than the one being aggregated for color, choosing a named
scheme — that ggplot2 either can't express in the plot call at all (pushing it
into upstream data code) or resolves to a different concrete default (scale
direction, exact hex stops) than the source library.