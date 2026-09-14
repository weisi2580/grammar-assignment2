library(ggplot2)
library(dplyr)

df <- read.csv("pr_data.csv")

# --- everything below is unchanged from translated_spec9.R (the raw LLM output) ---

df_binned <- df %>%
  mutate(hours_bin = floor(hours / 2) * 2) %>%
  group_by(hours_bin) %>%
  summarise(
    count = n(),
    mean_lines = mean(lines)
  )

p <- ggplot(df_binned, aes(x = hours_bin, y = count, fill = mean_lines)) +
  geom_col() +
  scale_fill_gradient(low = "#132B43", high = "#56B1F7") +
  labs(x = "review hours", y = "PR count", fill = "mean lines changed",
       title = "ggplot2 translation of Altair spec 9")

ggsave("spec9_ggplot2.png", p, width = 6, height = 4.5, dpi = 120)
cat("saved spec9_ggplot2.png\n")

# also save the same chart with the un-overridden ggplot2 default (removing
# the explicit scale_fill_gradient call) to see ggplot2's TRUE default,
# for a fair comparison against Altair's true default rendered earlier
p_default <- ggplot(df_binned, aes(x = hours_bin, y = count, fill = mean_lines)) +
  geom_col() +
  labs(x = "review hours", y = "PR count", fill = "mean lines changed",
       title = "ggplot2 TRUE default continuous scale (no override)")
ggsave("spec9_ggplot2_truedefault.png", p_default, width = 6, height = 4.5, dpi = 120)
cat("saved spec9_ggplot2_truedefault.png\n")
