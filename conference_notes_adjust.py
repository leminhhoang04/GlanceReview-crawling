import os
import json
from tqdm import tqdm

os.makedirs("./conference_notes_adjust", exist_ok=True)

conferences_notes = os.listdir("./conference_notes")

cnt = 0
for filename in tqdm(conferences_notes, desc="Adjusting conference notes"):
    filedir = os.path.join("./conference_notes", filename)
    with open(filedir, "r") as f:
        data = json.load(f)

    new_data = []
    for x in data:
        try:
            if filename.endswith("v1.json"):
                new_content = dict()
                #new_content["_bibtex"] = {
                #    "value": x["content"]["_bibtex"]
                #}
                new_content["title"] = {
                    "value": x["content"]["title"]
                }
                new_content["authors"] = {
                    "value": x["content"].get("authors", [])
                }
                #new_content["authorids"] = {
                #    "value": x["content"]["authorids"]
                #}
                new_content["keywords"] = {
                    "value": x["content"].get("keywords", [])
                }
                new_content["TLDR"] = {
                    "value": x["content"].get("TL;DR", "")
                }
                new_content["abstract"] = {
                    "value": x["content"].get("abstract", "")
                }
                new_content["pdf"] = {
                    "value": x["content"]["pdf"]
                }
                #new_content["venue"] = {
                #    "value": x["content"]["venue"]
                #}
                #new_content["venueid"] = {
                #    "value": x["content"]["venueid"]
                #}
                #new_content["paperhash"] = {
                #    "value": x["content"]["paperhash"]
                #}

                new_data.append({
                    "id": x["id"],
                    "forum": x["forum"],
                    "invitations": [
                        x["invitation"]
                    ],
                    #"cdate": x["cdate"],
                    #"odate": x["odate"],
                    #"mdate": x["mdate"],
                    #"signatures": x["signatures"],
                    #"writers": x["writers"],
                    #"readers": x["readers"],
                    "content": new_content,
                })
            else:
                new_content = dict()
                #new_content["_bibtex"] = x["content"]["_bibtex"]
                new_content["title"] = x["content"]["title"]
                new_content["authors"] = x["content"].get("authors", [])
                #new_content["authorids"] = x["content"]["authorids"]
                new_content["keywords"] = x["content"].get("keywords", [])
                new_content["TLDR"] = x["content"].get("TL;DR", "")
                new_content["abstract"] = x["content"].get("abstract", "")
                new_content["pdf"] = x["content"]["pdf"]
                #new_content["venue"] = x["content"]["venue"]
                #new_content["venueid"] = x["content"]["venueid"]
                #new_content["paperhash"] = x["content"]["paperhash"]

                new_data.append({
                    "id": x["id"],
                    "forum": x["forum"],
                    "invitations": x["invitations"],
                    #"cdate": x["cdate"],
                    #"odate": x["odate"],
                    #"mdate": x["mdate"],
                    #"signatures": x["signatures"],
                    #"writers": x["writers"],
                    #"readers": x["readers"],
                    "content": x["content"],
                })
        except:
            pass

    if len(new_data) > 0:
        with open(f"./conference_notes_adjust/{filename}", "w") as f:
            json.dump(new_data, f, indent=4)
        cnt += 1
    # if len=0, it shows that the conference has no pdf

print(f"{cnt}/{len(conferences_notes)}")