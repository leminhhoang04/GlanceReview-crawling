'''
python crawl_pdf.py --raw_notes conference_notes_adjust/ICLR.cc___2024___Conference___v2.json \
                    --root_dir pdfs/ICLR.cc___2024___Conference___v2 \
                    --api_version 2 --workers 8
'''
import os
import subprocess
import pandas as pd

df = pd.read_csv("icore-conf-rank-A-A*.csv", encoding="utf-8")
unique_acronyms = df['acronym'].dropna().unique().tolist()

conference_notes = 'conference_notes_adjust'
for conference in list(os.listdir(conference_notes)):
    found = any(acronym in conference for acronym in unique_acronyms)
    if not found:
        continue

    raw_notes = os.path.join(conference_notes, conference)
    root_dir = f'pdfs/{conference.replace(".json", "")}'
    api_version = conference[-6]
    workers = '8'

    print(f"Processing conference: {conference} using API version {api_version}")
    command = [
        'python', 'crawl_pdf.py',
        '--raw_notes', raw_notes,
        '--root_dir', root_dir,
        '--api_version', api_version,
        '--workers', workers
    ]
    subprocess.run(command)