'''
Hold notes that can be extracted into a json file
'''
import os
import json
import glob

output_dir = "conference_notes_adjust-extracted"
os.makedirs(output_dir, exist_ok=True)

for conference_notes_filename in os.listdir('conference_notes_adjust'):
    conference_notes_path = os.path.join('conference_notes_adjust', conference_notes_filename)
    conference_notes_name = conference_notes_filename[:-5]

    with open(conference_notes_path, 'r') as f:
        conference_notes = json.load(f)

    conference_notes_new = []
    for note in conference_notes:
        note_id = note["id"]
        if os.path.isfile(os.path.join("pdfs-extract", conference_notes_name, note_id + ".json")):
            conference_notes_new.append(note) # hold the note

    with open(os.path.join(output_dir, conference_notes_filename), 'w') as f:
        json.dump(conference_notes_new, f, indent=4, ensure_ascii=False)