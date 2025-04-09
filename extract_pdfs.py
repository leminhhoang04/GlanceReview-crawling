'''
python extract_pdf.py --conference_note_name ICLR.cc___2024___Conference___v2 --workers 32
'''
import os
import subprocess

log_file_path = "logs/extract_log.txt"
if os.path.exists(log_file_path):
    os.remove(log_file_path)

def main():
    conference_note_list = list(os.listdir("pdfs"))
    conference_note_list.sort()

    for conference_note in conference_note_list:
        string_info = f"Processing conference: {conference_note}"
        print(string_info)

        command = [
            'python', 'extract_pdf.py',
            '--conference_note_name', conference_note,
            '--workers', '32'
        ]

        with open(log_file_path, "a") as log_file:
            subprocess.run(['echo', f'\n{string_info}'], stdout=log_file, stderr=log_file)
            subprocess.run(command, stdout=log_file, stderr=log_file)

if __name__ == "__main__":
    main()