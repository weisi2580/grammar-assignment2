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
color scale.

**Raw translation** (unmodified LLM output): `translated_spec9.R`

**Run:** executed via `run_translated_spec9.R` (identical logic, with data
loading and `ggsave` calls added so it produces a comparable PNG) against
`pr_data.csv` — the exact same synthetic dataset used for the Altair specs,
exported so both languages plot identical numbers. Output: `spec9_ggplot2.png`
and `spec9_ggplot2_truedefault.png` (ggplot2's default with no color override,
for a fair default-vs-default comparison against Altair's spec 9).

## Divergence table

| Component | Source (Altair) behavior | Translated (ggplot2) behavior | Visible consequence |
|---|---|---|---|
| Binning + cross-variable aggregation | Vega-Lite bins `hours` and aggregates `mean(lines)` *within the same declarative encoding block* — one spec, no separate data step | ggplot2/`geom_col` has no way to bin one variable and aggregate a *different* variable into fill inside the plot call; the translation silently introduces a `dplyr` pre-aggregation step (`floor(hours/2)*2`, `group_by`, `summarise`) that lives outside the grammar entirely | The two charts can still end up looking identical, but the ggplot2 "spec" is no longer self-contained — the binning logic (and its edge convention) now lives in ordinary data-wrangling code the grammar can't check or reason about |
| Bin edge convention | Vega-Lite's `bin: {step: 2}` anchors bins at multiples of the step starting from a computed origin near the data minimum, with left-closed/right-open intervals | The translation's `floor(hours/2)*2` anchors bins at multiples of 2 starting at 0, also left-closed/right-open | For this dataset the two conventions happen to agree closely (values are far from 0), but they are not guaranteed to agree in general — a translator that trusts this pattern on a variable with a non-zero-friendly range would get silently shifted bin edges |
| Position ("stack") on a continuous-fill bar | `stack="zero"` is declared, but since `color` is a per-bin aggregate (one value per x-bin), there is only one mark per bin — stacking has no visible effect | `geom_col()`'s default position is also `"stack"`, and since the data was pre-aggregated to one row per bin, stacking likewise has no visible effect | **No divergence** — worth stating explicitly, since a translation that happens to match should be shown to match, not just assumed |
| Continuous color scale, direction | Altair's default continuous scheme (confirmed by rendering spec 9 with no `scheme` override) runs **light-at-low → dark-at-high** values | The translation, run and rendered as `spec9_ggplot2.png` / `spec9_ggplot2_truedefault.png`, runs **dark-at-low → light-at-high** — confirmed by direct visual comparison against `09.png`, not just by looking up the default | With both scales left at their true defaults, the *same* underlying values are encoded with opposite light/dark polarity — a bin with a low mean PR size looks pale in Altair and dark in ggplot2. This is a real "silently differing default," not an artifact of this translation, and would mislead a reader comparing the two figures side by side |
| Explicit `scheme="blues"` in the source | The source spec pins the scheme to `"blues"` rather than relying on Altair's true default | The translation instead reused ggplot2's own default gradient rather than reproducing Vega-Lite's specific `"blues"` ramp (a different set of hex stops) | Colors will be visibly different shades of blue for the same value, even though both are "blue" — an LLM translating a `scheme="blues"` string will often reach for the target library's own default blue rather than looking up Vega-Lite's actual `"blues"` color stops |

## Summary
Three of the five audited components diverge in ways that would produce a
visibly different figure from identical data (aggregation location, bin-edge
anchoring, and color-scale direction/stops); one component (stacking) matches
exactly and is reported as matching rather than omitted. The recurring pattern
is that Altair's single declarative encoding block does work — binning a
different variable than the one being aggregated for color, choosing a
canonical scheme name — that ggplot2 either can't express in the plot call at
all (pushing it into upstream data code) or resolves to a different concrete
default (scale direction, exact hex stops) than the source library.
