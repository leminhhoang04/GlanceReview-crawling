# read pdfs-extract -> json
# json["text"] -> text, references, appendix
# dump to pdfs-extract-final

import os
import json
from tqdm import tqdm

root_extracted = "pdfs-extract"
root_final = "pdfs-extract-final"
os.makedirs(root_final, exist_ok=True)

for venue in tqdm(os.listdir(root_extracted), desc="Dumping venues"):
    for paper in os.listdir(os.path.join(root_extracted, venue)):
        paper_path = os.path.join(root_extracted, venue, paper)
        # read json
        with open(paper_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # get text, references, appendix
        tmp = data["text"].split("References")
        text = tmp[0]
        tmp = "References".join(tmp[1:]).split("Appendix")
        references = tmp[0]
        appendix = "" if len(tmp) == 1 else "Appendix".join(tmp[1:])
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