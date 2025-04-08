'''
python crawl_pdf.py --raw_notes conference_notes_adjust/ICLR.cc___2024___Conference___v2.json \
                    --root_dir pdfs/ICLR.cc___2024___Conference___v2 \
                    --api_version 2 --workers 8
'''
import os
import json
import argparse
from tqdm import tqdm
from multiprocessing import Pool
from openreview_client import OpenReviewClient

def download_pdf(args):
    note, root_dir, api_version = args
    if note['content']['pdf']['value']:
        filepath = f'{root_dir}/{note["id"]}.pdf'
        if os.path.exists(filepath):
            return 1

        client = OpenReviewClient(api_version)
        # Retry logic
        for attempt in range(3):
            try:
                f = client.get_pdf(note["id"])
                with open(filepath,'wb') as op: 
                    op.write(f)
                return 1
            except (requests.exceptions.ChunkedEncodingError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.RequestException) as e:
                print(f"[Attempt {attempt+1}] Error downloading {note['id']}: {e}")
                time.sleep(2 * (attempt + 1))  # exponential backoff
        print(f"❌ Failed to download after retries: {note['id']}")
    return 0  # đánh dấu lỗi để dễ thống kê sau

def main():
    parser = argparse.ArgumentParser(description="Download PDFs from OpenReview notes.")
    parser.add_argument('--raw_notes',   type=str, required=True, help='Path to the raw notes JSON file')
    parser.add_argument('--root_dir',    type=str, required=True, help='Directory to save PDFs')
    parser.add_argument('--api_version', type=int, required=True, help='OpenReview API version (default: 2)')
    parser.add_argument('--workers',     type=int, default=8,     help='Number of parallel workers')
    args = parser.parse_args()

    os.makedirs(args.root_dir, exist_ok=True)
    with open(args.raw_notes, 'r') as f:
        notes = json.load(f)

    task_args = [(note, args.root_dir, args.api_version) for note in notes]
    with Pool(args.workers) as p:
        result = list(tqdm(p.imap(download_pdf, task_args), total=len(task_args), desc="Downloading PDFs"))
    print(f"Downloaded {len(result)} PDFs from {args.raw_notes} to {args.root_dir} using API version {args.api_version}.")

if __name__ == '__main__':
    main()