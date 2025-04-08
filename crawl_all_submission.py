from openreview_client import OpenReviewClient
from tqdm import tqdm
import json
import os

with open('venues.json', 'r') as f:
    venues = json.load(f)

for version in [2]:
    client = OpenReviewClient(version)
    for i, venue in tqdm(enumerate(venues), total=len(venues), desc=f'Version {version}'):
        filename = f'{venue}___v{version}.json'.replace('/', '___')
        filepath = os.path.join('conference_notes', filename)
        if os.path.exists(filepath):
            continue
        try:
            raw_notes = client.get_conference_notes(venue, active=False)
            json_notes = [note.to_json() for note in raw_notes]
            if len(json_notes) == 0:
                continue
            with open(filepath, 'w') as f:
                json.dump(json_notes, f, indent=2)
        except Exception as e:
            print(f'Error at {venue}: {e}')
            continue