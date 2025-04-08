from openreview_client import OpenReviewClient
import json

client = OpenReviewClient(1)
venues = client.get_all_venues()
print(len(venues))

client = OpenReviewClient(2)
venues = client.get_all_venues()
print(len(venues))

with open('venues.json', 'w', encoding='utf-8') as f:
    json.dump(venues, f, indent=2)