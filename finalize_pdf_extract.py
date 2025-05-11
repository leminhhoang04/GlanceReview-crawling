# read pdfs-extract -> json
# json["text"] -> text, references, appendix
# dump to pdfs-extract-final

import os
import re
import json
from multiprocessing import Pool
from tqdm import tqdm

root_extracted = "pdfs-extract"
root_final = "pdfs-extract-final"
os.makedirs(root_final, exist_ok=True)

def process_venue(data):
    root_final, root_extracted, venue = data
    for paper in os.listdir(os.path.join(root_extracted, venue)):
        paper_path = os.path.join(root_extracted, venue, paper)
        # read json
        with open(paper_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data["text"] = data["text"].replace(".sc/", "")
        # get text, references, appendix
        text = ""
        references = ""
        appendix = ""
        # splitting by last references and first appendi after last references
        text_lower = data["text"].lower()
        references_positions = [m.start() for m in re.finditer(r'references', text_lower)]
        if len(references_positions) == 0:
            references_positions = [m.start() for m in re.finditer(r'b?ibliography', text_lower)]
        if len(references_positions) == 0:
            references_positions = [m.start() for m in re.finditer(r'(?<![a-zA-Z])r?eference', text_lower)]
        if len(references_positions) == 0:
            references_positions = [m.start() for m in re.finditer(r'r.f.rences', text_lower)]
        if len(references_positions) == 0:
            references_positions = [m.start() for m in re.finditer(r'r\s?e\s?f\s?e\s?r\s?e\s?n\s?c\s?e\s?s', text_lower)]
        if len(references_positions) == 0:
            references_positions = [m.start() for m in re.finditer(r'r?eferencias', text_lower)]
        if len(references_positions) == 0:
            references_positions = [m.start() for m in re.finditer(r'literatur\n', text_lower)]

        if len(references_positions) > 0:
            ref_pos = references_positions[-1]
            text = data["text"][:ref_pos] # text | reference + appendix
            appendi_pos = text_lower.find("appendi", ref_pos)
            if appendi_pos != -1:
                references = data["text"][ref_pos:appendi_pos]
                appendix = data["text"][appendi_pos:]
            else:
                references = data["text"][ref_pos:]
        else:
            # khong co references = khong co appendix
            text = data["text"]
        # create new dict()
        d = dict()
        d["id"] = data["file_path"].split("/")[-1].split(".")[0]
        d["text"] = text
        d["references"] = references
        d["appendix"] = appendix
        # dump json
        os.makedirs(os.path.join(root_final, venue), exist_ok=True)
        with open(os.path.join(root_final, venue, paper), 'w', encoding='utf-8') as f:
            json.dump(d, f, indent=4)

parallel_data = []
for venue in tqdm(os.listdir(root_extracted), desc="Dumping venues"):
    parallel_data.append((root_final, root_extracted, venue))

# Parallel processing
with Pool(8) as p:
    result = list(tqdm(p.imap(process_venue, parallel_data), total=len(parallel_data), desc="Processing venues"))