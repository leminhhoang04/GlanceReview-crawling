from openreview_client import OpenReviewClient
from multiprocessing import Pool
from tqdm import tqdm
import requests
import json
import os

os.makedirs('pdfs', exist_ok=True)

def download_pdf(note):
    if note['content']['pdf']['value']:
        client = OpenReviewClient(2)
        filepath = f'pdfs/{note["id"]}.pdf'
        if os.path.exists(filepath):
            return 1
        f = client.get_attachment(note["id"], 'pdf')
        with open(filepath,'wb') as op: 
            op.write(f)
    return 1


client = OpenReviewClient(2)

raw_notes_list = ['conference_notes/NeurIPS.cc___2024___Conference___v2.json']
num_workers = 8
for raw_notes in raw_notes_list:
    with open(raw_notes, 'r') as f:
        notes = json.load(f)

    #for i, note in tqdm(enumerate(notes), total=len(notes), desc=f'{raw_notes}'):
    with Pool(num_workers) as p:
        result = list(tqdm(p.imap(download_pdf, notes), total=len(notes), desc="Downloading PDFs"))

print(len(result))