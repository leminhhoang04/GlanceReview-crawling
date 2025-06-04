import os
import json
import csv
import logging
from pathlib import Path
from typing import Dict, Any
from tqdm import tqdm

PROJECT_DIR = Path(__file__).resolve().parent
CONFERENCES_FOLDER = PROJECT_DIR / "conferences"
WRITEUP_DETAILS_FOLDER = PROJECT_DIR / "writeups"
CONFERENCE_INFO_FILE = PROJECT_DIR / "icore-conf-to-rank.csv"
CITATION_FILE = PROJECT_DIR / "citations_00000_68324.json"
OUTPUT_FOLDER = PROJECT_DIR / "processed_data"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


def load_conference_info() -> Dict[str, Dict[str, Any]]:
    """
    Load conference information from a CSV file.
    """
    conference_info = {}
    with open(CONFERENCE_INFO_FILE, 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            conference_info[row['conference_name']] = row
    logging.info(f"Loaded conference info for {len(conference_info)} conferences.")
    return conference_info


def load_citation_data() -> Dict[str, Dict[str, Any]]:
    """
    Load citation data from a JSON file.
    Convert the JSON data to a dictionary using the 'id' as the key.
    """
    with open(CITATION_FILE, 'r', encoding="utf-8") as jsonfile:
        citation_data = json.load(jsonfile)
    citation_data = {item['id']: item for item in citation_data}
    logging.info(f"Loaded citation data for {len(citation_data)} items.")
    return citation_data


def load_writeup_details_by_conf(conference_name: str) -> Dict[str, Dict[str, Any]]:
    """
    Load write up details for a specific conference from a folder.
    """
    writeup_details_folder = WRITEUP_DETAILS_FOLDER / conference_name
    writeup_details = {}
    for root, _, files in os.walk(writeup_details_folder):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding="utf-8") as jsonfile:
                    data = json.load(jsonfile)
                    writeup_details[data['id']] = data
    logging.info(f"Loaded {len(writeup_details)} writeup details for {conference_name}.")
    return writeup_details


def load_conference_notes(conference_name: str) -> Dict[str, Dict[str, Any]]:
    """
    Load conference notes from a json file.
    """
    conference_notes_file = CONFERENCES_FOLDER / f"{conference_name}.json"
    with open(conference_notes_file, 'r', encoding="utf-8") as jsonfile:
        conference_notes = json.load(jsonfile)
    conference_notes = {item['id']: item for item in conference_notes}
    logging.info(f"Loaded {len(conference_notes)} notes for {conference_name}.")
    return conference_notes


def main() -> None:
    conference_names = [
        file.rsplit('.', 1)[0]
        for file in os.listdir(CONFERENCES_FOLDER)
        if file.endswith('.json')
    ]
    logging.info(f"Found {len(conference_names)} conferences: {conference_names}")
    conference_info = load_conference_info()
    citation_data = load_citation_data()

    for conference_name in tqdm(conference_names, desc="Conferences"):
        logging.info(f"Processing conference: {conference_name}")
        writeup_details = load_writeup_details_by_conf(conference_name)
        conference_notes = load_conference_notes(conference_name)
        
        if len(conference_notes) != len(writeup_details):
            logging.warning(f"Mismatch in number of notes and writeup details for {conference_name}: "
                            f"{len(conference_notes)} notes, {len(writeup_details)} writeups")

        for note_id, note in tqdm(conference_notes.items(), desc=f"Notes ({conference_name})", leave=False):
            # Merge writeup details with conference notes
            if note_id in writeup_details:
                note.update(writeup_details[note_id])
            # Merge citation data with conference notes
            if note_id in citation_data:
                note.update(citation_data[note_id])
            # Add conference info to each note
            note.update(conference_info[conference_name])

        # Save the merged data to a new JSON file
        output_file = OUTPUT_FOLDER / f"{conference_name}.json"
        with open(output_file, 'w', encoding="utf-8") as jsonfile:
            json.dump(conference_notes, jsonfile, indent=4, ensure_ascii=False)
        logging.info(f"Saved merged data for {conference_name} to {output_file}")


if __name__ == "__main__":
    main()
