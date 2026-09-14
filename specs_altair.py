"""Assignment 2 — Build: ten specs, one grammar component changed per step,
from a single parent. Implemented in Altair (Vega-Lite). Run:
    python specs_altair.py
writes 00.png .. 10.png to ./out/
"""
import os
import altair as alt
from data import prs, monthly

alt.data_transformers.disable_max_rows()
OUT = "out"
os.makedirs(OUT, exist_ok=True)

df = prs()
m = monthly(df)


def save(i, chart):
    path = os.path.join(OUT, f"{i:02d}.png")
    chart.save(path)
    print("saved", path)


# ---------------------------------------------------------------------------
# 0 — PARENT: histogram of PR review hours, default binning
# ---------------------------------------------------------------------------
c0 = alt.Chart(df).mark_bar().encode(
    x=alt.X("hours:Q", bin=True, title="review hours"),
    y=alt.Y("count()", title="PR count"),
).properties(title="0 — parent: hours histogram, default bin")
save(0, c0)

# ---------------------------------------------------------------------------
# 1 — DEFAULTS made explicit: same stat+geom, explicit bin step
# ---------------------------------------------------------------------------
c1 = alt.Chart(df).mark_bar().encode(
    x=alt.X("hours:Q", bin=alt.Bin(step=2), title="review hours"),
    y=alt.Y("count()", title="PR count"),
).properties(title="1 — explicit binwidth (step=2) vs parent's default")
save(1, c1)

# ---------------------------------------------------------------------------
# 2 — GEOM swap: bar -> line (frequency polygon), same stat
# ---------------------------------------------------------------------------
c2 = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("hours:Q", bin=alt.Bin(step=2), title="review hours"),
    y=alt.Y("count()", title="PR count"),
).properties(title="2 — geom: bar -> line (frequency polygon)")
save(2, c2)

# ---------------------------------------------------------------------------
# 3 — GEOM swap (sibling of 2): bar -> tick (dot/strip-style display)
# ---------------------------------------------------------------------------
c3 = alt.Chart(df).mark_tick().encode(
    x=alt.X("hours:Q", bin=alt.Bin(step=2), title="review hours"),
    y=alt.Y("count()", title="PR count"),
).properties(title="3 — geom: bar -> tick (dot-style, Wickham's 'no name' geom)")
save(3, c3)

# ---------------------------------------------------------------------------
# 4 — STAT swap: bin+count -> bin+density (geom stays mark_bar)
# ---------------------------------------------------------------------------
c4 = alt.Chart(df).transform_bin("bin_hours", "hours", bin=alt.Bin(step=2)).transform_joinaggregate(
    total="count(*)"
).transform_calculate(
    density="1 / datum.total"
).mark_bar().encode(
    x=alt.X("bin_hours:Q", title="review hours"),
    x2="bin_hours_end:Q",
    y=alt.Y("sum(density):Q", title="density"),
).properties(title="4 — stat: count -> density (same bar geom)")
save(4, c4)

# ---------------------------------------------------------------------------
# 5 — COORDINATE transform: log10 on the x AXIS SCALE of the bar histogram
#     (kept separate from step 6's coordinate-transform-on-the-bin-edges point)
# ---------------------------------------------------------------------------
c5 = alt.Chart(df).mark_bar().encode(
    x=alt.X("hours:Q", bin=alt.Bin(step=2, extent=[1, 80]),
            scale=alt.Scale(type="log", domain=[1, 100]), title="review hours (log scale)"),
    y=alt.Y("count()", title="PR count"),
).properties(title="5 — scale: linear -> log10 (bins still computed on linear hours)")
save(5, c5)

# ---------------------------------------------------------------------------
# 6 — COORD transform proper: bin on log10(hours) directly (contrast with 5)
# ---------------------------------------------------------------------------
c6 = alt.Chart(df).transform_calculate(
    log_hours="log(datum.hours) / log(10)"
).mark_bar().encode(
    x=alt.X("log_hours:Q", bin=alt.Bin(step=0.1), title="log10(review hours)"),
    y=alt.Y("count()", title="PR count"),
).properties(title="6 — coord: bin edges computed on log10(hours) itself")
save(6, c6)

# ---------------------------------------------------------------------------
# 7 — FACET introduced (independent of layer, per Wickham)
# ---------------------------------------------------------------------------
c7 = alt.Chart(df).mark_bar().encode(
    x=alt.X("hours:Q", bin=alt.Bin(step=2), title="review hours"),
    y=alt.Y("count()", title="PR count"),
).properties(width=180, height=140).facet("repo:N", columns=2).properties(
    title="7 — facet: one panel per repo"
)
save(7, c7)

# ---------------------------------------------------------------------------
# 8 — POSITION: stacked bars, colour by kind (categorical scale)
# ---------------------------------------------------------------------------
c8 = alt.Chart(df).mark_bar().encode(
    x=alt.X("hours:Q", bin=alt.Bin(step=2), title="review hours"),
    y=alt.Y("count()", stack="zero", title="PR count"),
    color=alt.Color("kind:N", title="PR kind"),
).properties(title="8 — position: stacked, coloured by kind (categorical scale)")
save(8, c8)

# ---------------------------------------------------------------------------
# 9 — SCALE change on the same encoding: categorical colour -> continuous colour
#     (mean PR size per bin), still stacked bars
# ---------------------------------------------------------------------------
c9 = alt.Chart(df).mark_bar().encode(
    x=alt.X("hours:Q", bin=alt.Bin(step=2), title="review hours"),
    y=alt.Y("count()", stack="zero", title="PR count"),
    color=alt.Color("mean(lines):Q", scale=alt.Scale(scheme="blues"), title="mean lines changed"),
).properties(title="9 — scale: categorical colour -> continuous colour (mean PR size)")
save(9, c9)

# ---------------------------------------------------------------------------
# 10 — GRAMMAR AS INTERFACE: same components, entirely different chart type
#      by swapping which variables are mapped where (distribution -> relationship)
# ---------------------------------------------------------------------------
c10 = alt.Chart(df).mark_circle(opacity=0.35).encode(
    x=alt.X("lines:Q", scale=alt.Scale(type="log"), title="lines changed (log)"),
    y=alt.Y("hours:Q", scale=alt.Scale(type="log"), title="review hours (log)"),
    color=alt.Color("repo:N", title="repo"),
).properties(title="10 — same grammar, different question: distribution -> relationship")
save(10, c10)