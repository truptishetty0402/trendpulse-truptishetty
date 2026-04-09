"""
TrendPulse - Task 3
Analyze the cleaned CSV dataset using Pandas and NumPy.

Steps:
1. Load the cleaned CSV file
2. Perform statistical analysis
3. Identify trending categories
4. Calculate average scores and comments
"""

import pandas as pd
import numpy as np
import os

DATA_FOLDER = "data"


def find_latest_csv():
    """
    Find the latest cleaned CSV file created in Task 2.
    """
    files = [f for f in os.listdir(DATA_FOLDER) if f.startswith("trends_cleaned_") and f.endswith(".csv")]

    if not files:
        print("No cleaned CSV file found.")
        return None

    files.sort()
    return os.path.join(DATA_FOLDER, files[-1])


def main():

    # Step 1: Locate latest CSV file
    csv_file = find_latest_csv()

    if not csv_file:
        return

    print(f"Loading cleaned data from {csv_file}")

    # Step 2: Load data
    df = pd.read_csv(csv_file)

    print("\nTotal Stories:", len(df))

    # Step 3: Category distribution
    print("\nStories per Category:")
    category_counts = df["category"].value_counts()
    print(category_counts)

    # Step 4: Average score per category
    print("\nAverage Score per Category:")
    avg_scores = df.groupby("category")["score"].mean()
    print(avg_scores)

    # Step 5: Average comments per category
    print("\nAverage Comments per Category:")
    avg_comments = df.groupby("category")["num_comments"].mean()
    print(avg_comments)

    # Step 6: Find most popular story
    top_story = df.loc[df["score"].idxmax()]

    print("\nTop Trending Story:")
    print("Title:", top_story["title"])
    print("Category:", top_story["category"])
    print("Score:", top_story["score"])
    print("Author:", top_story["author"])

    # Step 7: Use NumPy for additional stats
    print("\nNumPy Statistics:")
    print("Max Score:", np.max(df["score"]))
    print("Min Score:", np.min(df["score"]))
    print("Mean Score:", np.mean(df["score"]))
    print("Median Score:", np.median(df["score"]))


if __name__ == "__main__":
    main()
