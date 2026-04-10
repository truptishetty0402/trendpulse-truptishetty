# Task 4: Visualizations

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# ---------------- Chart 1 ----------------
top10 = df.nlargest(10, "score")

# Shorten titles
top10["title"] = top10["title"].apply(lambda x: x[:50])

plt.figure()
plt.barh(top10["title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Title")
plt.title("Top 10 Stories by Score")
plt.savefig("outputs/chart1_top_stories.png")

# ---------------- Chart 2 ----------------
plt.figure()
df["category"].value_counts().plot(kind="bar")
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.savefig("outputs/chart2_categories.png")

# ---------------- Chart 3 ----------------
plt.figure()

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Comments")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")

# ---------------- Dashboard ----------------
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Chart 1
axs[0].barh(top10["title"], top10["score"])
axs[0].set_title("Top Stories")

# Chart 2
df["category"].value_counts().plot(kind="bar", ax=axs[1])
axs[1].set_title("Categories")

# Chart 3
axs[2].scatter(df["score"], df["num_comments"])
axs[2].set_title("Score vs Comments")

fig.suptitle("TrendPulse Dashboard")

plt.savefig("outputs/dashboard.png")

print("All charts saved in outputs/")
