# Raw translation of specs_altair.py spec #9 into ggplot2.
# Source (Altair):
#
# alt.Chart(df).mark_bar().encode(
#     x=alt.X("hours:Q", bin=alt.Bin(step=2)),
#     y=alt.Y("count()", stack="zero"),
#     color=alt.Color("mean(lines):Q", scale=alt.Scale(scheme="blues"))
# )
#
# Translated by Claude (Tier-1, raw output, unmodified):

library(ggplot2)
library(dplyr)

# Altair computes both the bin and the two aggregates (count, mean(lines))
# declaratively inside the encoding. ggplot2 has no direct equivalent that
# bins on one axis while aggregating a *different* continuous variable into
# fill, so the aggregation has to be done by hand before plotting.

df_binned <- df %>%
  mutate(hours_bin = floor(hours / 2) * 2) %>%
  group_by(hours_bin) %>%
  summarise(
    count = n(),
    mean_lines = mean(lines)
  )

ggplot(df_binned, aes(x = hours_bin, y = count, fill = mean_lines)) +
  geom_col() +
  scale_fill_gradient(low = "#132B43", high = "#56B1F7") +
  labs(x = "review hours", y = "PR count", fill = "mean lines changed")
