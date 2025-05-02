import os
import re
import csv
import pandas as pd

conference_notes_list = list(os.listdir('conference_notes_adjust-extracted'))
conference_notes_list = [note[:-5] for note in conference_notes_list] # remove .json suffix

df = pd.read_csv('icore-conf-rank.csv')
df = df.sort_values(by='rank')
df = df[df['acronym'].notna()]  # bỏ NaN
df = df[df['acronym'].str.strip() != '']  # bỏ chuỗi trắng
acronym_to_rank = dict(zip(df['acronym'], df['rank']))


d = dict()
for conference_notes_name in conference_notes_list:
    acronyms = []
    for i, acronym in enumerate(acronym_to_rank.keys()):
        parts = re.split(r'[_\.]+', conference_notes_name)
        if acronym in parts:
            acronyms.append((i, acronym, acronym_to_rank[acronym]))
    if len(acronyms) == 0:
        acronyms.append((-1, "404", "not-icore"))
    #if len(acronyms) > 1:
    #    print(conference_notes_name, acronyms)
    d[conference_notes_name] = acronyms[0]
d['roboticsfoundation.org___RSS___2024___Workshop___DM___v2'] = (1961, 'RSS', 'TBR')


with open('icore-conf-to-rank.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Ghi tiêu đề (header)
    writer.writerow(['conference_name', 'acronym', 'rank'])
    # Duyệt qua dict và ghi vào CSV
    for conference_name, (id, acronym, rank) in d.items():
        writer.writerow([conference_name, acronym, rank])
print("Done")