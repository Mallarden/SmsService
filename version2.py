import requests
import hashlib
import time
import feedparser
import keys


# Define the URL of the website
url = 'https://www.livsmedelsverket.se/rss/rss-aterkallanden'

# Define your 46elks API credentials
api_username = keys.elk_username
api_password = keys.elk_password

# Define the list of phone numbers to send the SMS to
phone_numbers = ['+46700299259', '+4687654321', '+46708782688']

# Continuously check the website every one minute
while True:
    # Fetch and hash the current website content
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        hashed_content = hashlib.md5(content).hexdigest()
    else:
        print('Failed to fetch the website content.')
        continue

    # Read the last hashed content from a file
    try:
        with open('last_hash.txt', 'r') as file:
            last_hash = file.read().strip()
    except FileNotFoundError:
        last_hash = None

    # Check if the website has changed
    if last_hash and hashed_content == last_hash:
        print('The website has not changed.')
    else:
        # Save the new hashed content to the file
        with open('last_hash.txt', 'w') as file:
            file.write(hashed_content)

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

                # Remove the character ' (apostrophe) from the feed entry description
                entry_description = entry.description.replace("'", "")
                
                # Concatenate the feed entry details to the feed_entries string
                feed_entries += f"Info: {entry.description}\n"
                feed_entries += f"Datum: {date_without_timezone}\n"
                feed_entries += "---\n"
    
        """
        # Send the RSS feed via SMS to each number in the list
        for phone_number in phone_numbers:
            api_url = 'https://api.46elks.com/a1/sms'
            data = {
                'from': 'Varning',
                'to': phone_number,
                'message': feed_entries
            }
            response = requests.post(api_url, auth=(api_username, api_password), data=data)

            # Check the response status
            if response.status_code == 201:
                print(f'SMS sent successfully to {phone_number}.')
            else:
                print(f'Failed to send the SMS to {phone_number}.')
                """
        print(feed_entries)

    # Wait for one minute before checking again
    time.sleep(60)
