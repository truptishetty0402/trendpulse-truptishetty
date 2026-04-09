"""
TrendPulse - Task 1 (Final Simplified Version)

Fetch trending stories from HackerNews API,
categorize them, and save 100+ stories.

Author: Trupti Shetty
"""

import requests
import json
import os
import time
from datetime import datetime

# API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories with keywords
categories = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["nfl","nba","fifa","sport","team","player","league","match"],
    "science": ["research","study","space","physics","biology","discovery","nasa"],
    "entertainment": ["movie","film","music","netflix","book","show","award","tv"]
}


def get_category(title):
    """Assign category based on keywords"""
    title_lower = title.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return "technology"   # 🔥 fallback ensures no story is lost


def fetch_json(url):
    """Safe API request"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        print(f"Request failed: {url}")
        return None


def main():

    print("Fetching top stories...")

    story_ids = fetch_json(TOP_STORIES_URL)

    if not story_ids:
        print("Failed to fetch story IDs")
        return

    # 🔥 Increased range ensures enough data
    story_ids = story_ids[:1500]

    collected = []

    for i, story_id in enumerate(story_ids):

        # Stop once we have enough stories
        if len(collected) >= 120:
            break

        story = fetch_json(ITEM_URL.format(story_id))

        if not story:
            continue

        title = story.get("title", "")

        if not title:
            continue

        category = get_category(title)

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

        # Sleep every 50 requests (rate safety)
        if i % 50 == 0:
            time.sleep(2)

    # Create data folder
    os.makedirs("data", exist_ok=True)

    # File name
    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{today}.json"

    # Save file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=2)

    # Final output
    print(f"Collected {len(collected)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
