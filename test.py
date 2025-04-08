import os
import json
import pandas as pd

##################################################

arr = list(os.listdir('conference_notes'))
print("# of crawled conferences:", len(arr))

cnt = 0
for conf in arr:
    with open(f'conference_notes/{conf}', 'r') as f:
        data = json.load(f)
        cnt += len(data)
print("# of papers:", cnt)

##################################################
print('#' * 20)

df = pd.read_csv("icore-conf-rank-A-A*.csv", encoding="utf-8")
unique_acronyms = df['acronym'].dropna().unique().tolist()
print("# of unique acronyms:", len(unique_acronyms))

arr = list(os.listdir('conference_notes'))
print("# of crawled conferences:", len(arr))

cnt = 0
cnt_conf = 0
for conf in arr:
    found = any(acronym in conf for acronym in unique_acronyms)
    if not found:
        continue

    cnt_conf += 1
    with open(f'conference_notes/{conf}', 'r') as f:
        data = json.load(f)
        cnt += len(data)
print("# of conferences A, A*:", cnt_conf)
print("# of papers A, A*:", cnt)

##################################################
print('#' * 20)

arr = list(os.listdir('pdfs/'))
print("# of crawled pdfs:", len(arr))

import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):  # Kiểm tra nếu là file
                total_size += os.path.getsize(file_path)
    return total_size

folder_path = "pdfs/"  # Thay đường dẫn thư mục của bạn
size_in_bytes = get_folder_size(folder_path)

# Chuyển đổi sang đơn vị dễ đọc (KB, MB, GB)
def convert_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

print(f"Folder size: {convert_size(size_in_bytes)}")




print('#' * 20)

arr = list(os.listdir('pdfs-extract/'))
print("# of crawled pdfs-extract:", len(arr))

folder_path = "pdfs-extract/"  # Thay đường dẫn thư mục của bạn
size_in_bytes = get_folder_size(folder_path)

# Chuyển đổi sang đơn vị dễ đọc (KB, MB, GB)
def convert_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

print(f"Folder size: {convert_size(size_in_bytes)}")
