"""
TrendPulse - Task 4
Visualize the analyzed trending data using charts.

Steps:
1. Load the cleaned CSV file
2. Create visualizations for:
   - Number of stories per category
   - Average score per category
   - Average comments per category
"""

import pandas as pd
import matplotlib.pyplot as plt
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

    # Step 1: Load the cleaned dataset
    csv_file = find_latest_csv()

    if not csv_file:
        return

    print(f"Loading data from {csv_file}")

    df = pd.read_csv(csv_file)

    # -------- Chart 1: Stories per Category --------
    category_counts = df["category"].value_counts()

    plt.figure()
    category_counts.plot(kind="bar")

    plt.title("Number of Trending Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")

    plt.tight_layout()
    plt.show()

    # -------- Chart 2: Average Score per Category --------
    avg_scores = df.groupby("category")["score"].mean()

    plt.figure()
    avg_scores.plot(kind="bar")

    plt.title("Average Score per Category")
    plt.xlabel("Category")
    plt.ylabel("Average Score")

    plt.tight_layout()
    plt.show()

    # -------- Chart 3: Average Comments per Category --------
    avg_comments = df.groupby("category")["num_comments"].mean()

    plt.figure()
    avg_comments.plot(kind="bar")

    plt.title("Average Comments per Category")
    plt.xlabel("Category")
    plt.ylabel("Average Comments")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
