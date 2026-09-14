# AI-LOG

**Course:** CS 8630 | **Student:** Weisi | **Project/Assignment:** Assignment 2 — One Dataset, Ten Specifications

---

### [2026-09-13] — Essay: word-count expansion and structure feedback

- **Tool/model:** Claude Sonnet 4.6
- **What I asked for:** my draft essay (Wilkinson vs. Wickham comparison + closing argument) was at 666 words against a 1,000-word target; I asked where the argument had room to go deeper rather than just be padded, and for a transition sentence summarizing what Wickham's departures buy overall.
- **What it produced:** section-by-section suggestions (an intro motivation gap, a missing concrete example in the stat/geom section, a missing cost/benefit framing for defaults, and a suggestion to tie the coordinate/faceting section to Wilkinson's own pie-chart chapter), plus one drafted transition paragraph (~60 words) synthesizing "what these departures buy."
- **Accepted:** the transition paragraph, used close to verbatim as the bridge before my closing argument. The suggestion to cite Wilkinson's Ch.2 "How to Make a Pie" directly in my coordinate/faceting paragraph, since it lines up with my own closing example.
- **Rejected/modified:** I did the actual expansion writing myself in each section (motivation, examples, cost/benefit framing) rather than taking AI-drafted paragraphs for those — I only used the one explicitly-requested synthesis paragraph as provided.
- **Verification:** re-read the full essay after inserting the transition paragraph to confirm it matched my own prose register and didn't introduce claims I hadn't verified against the assigned readings myself.

---

### [2026-09-13] — Ten Altair specs for Assignment 2 build

- **Tool/model:** Claude Sonnet 4.6
- **What I asked for:** I chose the dataset (synthetic Augur PR extract), the parent spec (histogram of PR review hours), and the full plan for which grammar component each of the ten specs should vary (geom swap, stat swap, the scale-vs-coordinate log pair, facet by repo, position/color, continuous color scale, and a final distribution→relationship reframe). I asked AI to write the Altair syntax implementing that plan.
- **What it produced:** a working Python script (`specs_altair.py`) with all ten specs, rendered PNGs, and a draft two-sentence annotation for each.
- **Accepted:** the Altair syntax itself (bin specs, mark types, encoding channels) after running it and confirming each chart rendered as intended.
- **Rejected/modified:** rewrote the annotations for `specs.md` myself after running the code and looking at the actual generated images — the initial AI-drafted wording described what the code was supposed to do, not necessarily what the rendered chart actually showed, so I checked each image against its annotation and adjusted the wording to match what I could actually see.
- **Verification:** ran `specs_altair.py` myself, inspected all eleven output images, and one bug (blank chart) was caught and fixed (log-scale axis had a zero-domain issue with the bin edges) before finalizing.

---

### [2026-09-13] — Translation audit (Tier 1): Altair spec 9 → ggplot2

- **Tool/model:** Claude Sonnet 4.6
- **What I asked for:** translate my most complex spec (spec 9: binned count, stacked position, continuous color scale on mean PR size) from Altair into ggplot2.
- **What it produced:** raw R/ggplot2 translation code (`translated_spec9.R`), kept unmodified in the repo per the Tier-1 rule.
- **Accepted:** the raw translation as-is, unmodified, as required for Tier-1 submissions.
- **Rejected/modified:** N/A for the code itself; the divergence analysis in `translation-audit.md` was written after running the translation and is a separate documentation step, not a change to the raw output.
- **Verification:** ran the translated R code, rendered the chart, and visually compared it against the Altair original — confirmed one real divergence (the two libraries' default continuous color scales run in opposite light/dark directions) and one non-divergence (position="stack" has no visible effect in either library once the data is pre-aggregated to one row per bin).
