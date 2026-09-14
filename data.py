"""Same synthetic Augur-PR dataset as the course's _grammar.py::prs()/monthly(),
reimplemented here (project files are read-only) so this script is self-contained."""
import numpy as np
import pandas as pd


def prs():
    """Per-PR records for four repos over 24 months: the course dataset."""
    rng = np.random.default_rng(2)
    rows = []
    for repo, base, growth in [("augur", 30, 0.9), ("frontend", 18, 1.4), ("docs", 8, 0.1), ("cli", 12, 0.6)]:
        for m in range(24):
            n = max(2, int(base + growth * m + 6 * np.sin(m / 2.5) + rng.normal(0, 3)))
            for _ in range(n):
                size = rng.lognormal(4, 1)                                      # lines changed
                lat = np.exp(0.9 + 0.35 * np.log(size) + rng.normal(0, .5))     # review hours
                rows.append(dict(repo=repo, month=m, lines=size, hours=lat,
                                  kind=rng.choice(["feature", "fix", "docs"], p=[.4, .45, .15])))
    return pd.DataFrame(rows)


def monthly(df):
    return df.groupby(["repo", "month"], as_index=False).size().rename(columns={"size": "prs"})


if __name__ == "__main__":
    df = prs()
    print(df.shape)
    print(df.head())
    print(df["hours"].describe())
