"""
TrendPulse - Task 2
Load the JSON file created in Task 1, clean the data,
and save it as a CSV file.

Steps:
1. Load JSON data
2. Convert it into a pandas DataFrame
3. Clean the data (remove duplicates, handle missing values)
4. Save the cleaned dataset as CSV
"""

import pandas as pd
import json
import os
from datetime import datetime

# Folder where JSON file from Task 1 is stored
DATA_FOLDER = "data"

def find_latest_json():
    """
    Find the latest trends JSON file inside the data folder.
    """
    files = [f for f in os.listdir(DATA_FOLDER) if f.startswith("trends_") and f.endswith(".json")]

    if not files:
        print("No JSON file found in data folder.")
        return None

    # Sort files and pick the latest
    files.sort()
    return os.path.join(DATA_FOLDER, files[-1])


def main():

    # Step 1: Locate JSON file from Task 1
    json_file = find_latest_json()

    if not json_file:
        return

    print(f"Loading data from {json_file}")

    # Step 2: Load JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Step 3: Convert to pandas DataFrame
    df = pd.DataFrame(data)

    print("Original records:", len(df))

    # Step 4: Data Cleaning

    # Remove duplicate posts
    df = df.drop_duplicates(subset="post_id")

    # Remove rows with missing titles
    df = df.dropna(subset=["title"])

    # Convert collected_at to datetime
    df["collected_at"] = pd.to_datetime(df["collected_at"])

    # Reset index after cleaning
    df = df.reset_index(drop=True)

    print("Cleaned records:", len(df))

    # Step 5: Save cleaned dataset to CSV
    today = datetime.now().strftime("%Y%m%d")
    csv_file = f"{DATA_FOLDER}/trends_cleaned_{today}.csv"

    df.to_csv(csv_file, index=False)

    print(f"Cleaned data saved to {csv_file}")


if __name__ == "__main__":
    main()
