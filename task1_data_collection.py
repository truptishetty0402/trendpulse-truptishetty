# Task 1: Fetch Data from HackerNews API
# Author: Tupti Ashish Shetty

import requests
import json
import time
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"Trupti": "TrendPulse/1.0"}

# Categories and keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Store collected stories
collected_stories = []

def get_category(title):
    """Assign category based on keywords"""
    title_lower = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    story_ids = response.json()[:500]
except Exception as e:
    print("Error fetching top stories:", e)
    story_ids = []

# Collect up to 25 per category
category_counts = {cat: 0 for cat in categories}

for story_id in story_ids:
    try:
        res = requests.get(ITEM_URL.format(story_id), headers=headers)
        story = res.json()
    except:
        print(f"Failed to fetch story {story_id}")
        continue

    if not story or "title" not in story:
        continue

    category = get_category(story["title"])
    if not category:
        continue

    if category_counts[category] >= 25:
        continue

    data = {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    collected_stories.append(data)
    category_counts[category] += 1

    # Stop if all categories filled
    if all(count >= 25 for count in category_counts.values()):
        break

# Create data folder
if not os.path.exists("data"):
    os.makedirs("data")

# Save file
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as f:
    json.dump(collected_stories, f, indent=4)

print(f"Collected {len(collected_stories)} stories. Saved to {filename}")
