# Task 3: Analysis with Pandas & NumPy

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("data/trends_clean.csv")

print("Loaded data:", df.shape)

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Averages
print("\nAverage score:", df["score"].mean())
print("Average comments:", df["num_comments"].mean())

# NumPy analysis
scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean:", np.mean(scores))
print("Median:", np.median(scores))
print("Std Dev:", np.std(scores))
print("Max:", np.max(scores))
print("Min:", np.min(scores))

# Most stories category
print("\nMost stories in:")
print(df["category"].value_counts().idxmax())

# Most commented story
top_comment = df.loc[df["num_comments"].idxmax()]
print("\nMost commented story:")
print(top_comment["title"], "-", top_comment["num_comments"])

# Add columns
df["engagement"] = df["num_comments"] / (df["score"] + 1)

avg_score = df["score"].mean()
df["is_popular"] = df["score"] > avg_score

# Save
df.to_csv("data/trends_analysed.csv", index=False)

print("\nSaved to data/trends_analysed.csv")
