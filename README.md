# Assignment 2 — One Dataset, Ten Specifications

## Files

- **`essay.md`** — comparison essay (Wilkinson vs. Wickham) + closing argument.
- **`specs.md`** — the ten specs: code, rendered chart, and annotation for each (images referenced from `out/`).
- **`translation-audit.md`** — Tier-1 divergence table for the Altair → ggplot2 translation.
- **`AI-LOG.md`** — AI collaboration log.

## Environment

- Python: `altair`, `vl-convert-python`, `pandas`
- R: `ggplot2`, `dplyr`

## How to run

```bash
# generate the ten specs (writes out/00.png..10.png and out/specs.md)
pip install altair vl-convert-python pandas
python3 specs_altair.py

# run the ggplot2 translation (writes spec9_ggplot2.png)
Rscript run_translated_spec9.R
```

`translated_spec9.R` is the raw, unmodified LLM translation (Tier-1
requirement); `run_translated_spec9.R` is the same code with data-loading and
`ggsave` added so it can actually be executed. `pr_data.csv` is the dataset
exported from `data.py` so both languages plot identical numbers.
