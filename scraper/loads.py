import requests
import csv

API_KEY = ""
VIDEO_ID = "REvlWJ7lo4M"

base_url = "https://www.googleapis.com/youtube/v3/commentThreads"
params = {
    "part": "snippet,replies",
    "videoId": VIDEO_ID,
    "key": API_KEY,
    "maxResults": 100
}

all_comments = []
next_page_token = None

while True:
    if next_page_token:
        params["pageToken"] = next_page_token
    else:
        params.pop("pageToken", None)  # Remove if not needed

    response = requests.get(base_url, params=params)
    data = response.json()

    # Parse top-level comments
    for item in data.get("items", []):
        top_snippet = item["snippet"]["topLevelComment"]["snippet"]
        all_comments.append({
            "author": top_snippet["authorDisplayName"],
            "comment": top_snippet["textDisplay"]
        })

        # Parse replies if available
        if "replies" in item:
            for reply in item["replies"]["comments"]:
                reply_snippet = reply["snippet"]
                all_comments.append({
                    "author": reply_snippet["authorDisplayName"],
                    "comment": reply_snippet["textDisplay"]
                })

    # Pagination
    next_page_token = data.get("nextPageToken")
    if not next_page_token:
        break

# Save to CSV
with open("youtube_comments.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["author", "comment"])
    writer.writeheader()
    writer.writerows(all_comments)

print(f"✅ Scraped {len(all_comments)} comments and saved to youtube_comments.csv")
