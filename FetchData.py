import feedparser
import re

url = 'https://www.livsmedelsverket.se/rss/rss-aterkallanden'

# Fetch the RSS feed
feed = feedparser.parse(url)

# Check if the feed was fetched successfully
if feed.entries:
    # Create an empty string variable to store the feed entries
    feed_entries = ""
    
    # Iterate over the feed items
    for entry in feed.entries:
        # Remove the timezone information from the published field
        date_without_timezone = entry.published.split("+")[0]
        
        # Concatenate the feed entry details to the feed_entries string
        feed_entries += f"{entry.description}\n"
        feed_entries += f"{date_without_timezone}\n"
        feed_entries += "---\n"
    
    # Print the complete feed entries
    feed_entries = feed_entries.replace('’', '')
    print(feed_entries)
else:
    print("Failed to fetch the RSS feed")
