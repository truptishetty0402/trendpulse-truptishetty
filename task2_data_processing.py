# Task 2: Clean JSON data and save as CSV

import pandas as pd
import os

# Load latest JSON file
file_path = "/content/data/trends_20260410.json"  # update date if needed

df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories")

# Remove duplicates
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove nulls
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# Remove low scores
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Clean title whitespace
df["title"] = df["title"].str.strip()

# Save CSV
output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

# Summary
print("\nStories per category:")
print(df["category"].value_counts())
