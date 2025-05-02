# read conferences_notes_adjust-extracted
# add "pdf-public" attribute
# save to conferences_notes_adjust-final

import os
import json
from tqdm import tqdm

root_extracted = "conference_notes_adjust-extracted"
root_final = "conference_notes_adjust-final"
os.makedirs(root_final, exist_ok=True)

map_version_baseurl = {
    "v1": "https://api.openreview.net",
    "v2": "https://api2.openreview.net",
}

conference_notes = os.listdir(root_extracted)
for notes in tqdm(conference_notes, desc="Dumping notes"):
    version = notes[-7:-5]
    # read note
    notes_path = os.path.join(root_extracted, notes)
    with open(notes_path, 'r', encoding='utf-8') as f:
        note_list = json.load(f)
    # add attribute
    updated_note_list = []
    for note in note_list:
        # collect data
        is_accepted = False
        for invitation in note["invitations"]:
            if "camera_ready" in invitation.lower():
                is_accepted = True
        # add attributes
        note["content"]["pdf-public"] = {
            "value": map_version_baseurl[version] + note["content"]["pdf"]["value"]
        }
        note["content"]["is_accepted"] = {
            "value": is_accepted
        }
        updated_note_list.append(note)
    # dump note
    with open(os.path.join(root_final, notes), 'w', encoding='utf-8') as f:
        json.dump(updated_note_list, f, indent=4)