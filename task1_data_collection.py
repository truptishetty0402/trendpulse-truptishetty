"""
TrendPulse - Task 1
Fetch trending stories from HackerNews API and categorize them.

Steps:
1. Fetch top story IDs
2. Fetch each story's details
3. Categorize stories using keywords
4. Collect max 25 stories per category
5. Save results to JSON file inside data/ folder
"""

import requests
import json
import os
import time
from datetime import datetime

# HackerNews API endpoints
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required header
headers = {"User-Agent": "TrendPulse/1.0"}

# Keywords used to categorize stories
categories = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment": ["movie","film","music","netflix","game","book","show","award","streaming"]
}

MAX_PER_CATEGORY = 25


def get_category(title):
    """
    Check story title and assign category based on keywords.
    Returns category name or None if no match found.
    """
    title_lower = title.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None


def fetch_json(url):
    """
    Helper function to safely fetch JSON data from API.
    If request fails, print message and return None.
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        print(f"Request failed: {url}")
        return None


def main():

    print("Fetching top stories...")

    # Step 1: Fetch top story IDs
    story_ids = fetch_json(TOP_STORIES_URL)

    if not story_ids:
        print("Could not fetch top stories.")
        return

    # Only take first 500 IDs
    story_ids = story_ids[:500]

    collected = []
    category_counts = {cat: 0 for cat in categories}

    # Step 2: Fetch each story's details
    for story_id in story_ids:

        # Stop when all categories reach limit
        if all(count >= MAX_PER_CATEGORY for count in category_counts.values()):
            break

        story = fetch_json(ITEM_URL.format(story_id))

        if not story:
            continue

        title = story.get("title", "")

        if not title:
            continue

        category = get_category(title)

        if category is None:
            continue

        if category_counts[category] >= MAX_PER_CATEGORY:
            continue

        # Step 3: Extract required fields
        record = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().isoformat()
        }

        collected.append(record)
        category_counts[category] += 1

        # Wait 2 seconds after finishing a category
        if category_counts[category] == MAX_PER_CATEGORY:
            print(f"Collected 25 stories for {category}")
            time.sleep(2)

    # Step 4: Create data folder if not exists
    os.makedirs("data", exist_ok=True)

    # Create filename with date
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"

    # Step 5: Save stories to JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=2)

    print(f"\nCollected {len(collected)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
