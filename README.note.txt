# conference_notes/

Mỗi file trong folder chứa submissions của venue tương ứng
Mỗi file có đuôi __v1 hoặc __v2 ứng với đã sử dụng API_v1/v2 khi crawling

# conference_notes_adjust/

Loại bỏ sự khác nhau của v1 và v2
Có các giá trị sau: id, forum, invitations, content {title, authors, keywords, TLDR, abstract, pdf}

# conference_notes_adjust-extracted/

Chỉ giữ lại những note có thể extract thành JSON trong pdfs-extract/

# conference_notes_adjust-final/

thêm attributes: "pdf-public" và "is_accepted"

# pdfs/

Hiện tại đã crawl 4035 file pdf ứng với venue "conference_notes/NeurIPS.cc___2024___Conference___v2.json"
Mỗi file có filename ứng với id của paper (note) tương ứng
Ví dụ: file "pdfs/5fybcQZ0g4.pdf" là pdf của paper (note) có id là "5fybcQZ0g4"

# pdfs-extract/

Với mỗi pdf trong pdfs/, extract text và table thành JSON

# pdf-extract-final/

Bỏ "table", tách "text" thành "text", "references", và "appendix"


# icore-conf-rank.csv và icore-conf-rank-A-A*.csv

chứa dữ liệu của các conference được crawl từ icore
- có các thông tin: index, conference_name, acronym, rank, url


# ranking: icore-conf-to-rank.csv

conference_name,acronym,rank
aclweb.org___ACL___ARR___2021___November___v1,ACL,A*
icaps-conference.org___ICAPS___2019___Workshop___WIPC___v1,ICAPS,A*
...
NeurIPS.cc___2022___Workshop___DistShift___v1,NeurIPS,A*
ICLR.cc___2025___Workshop___MCDC___v2,ICLR,A*


# python source codes

- get_icore_conference_rank.py:
  + request vào icore website để crawl data
  + output được lưu vào `icore-conf-rank.csv`
- get_icore_conference_rank_filter.py
  + filter các conference rank A/A*
  + output được lưu vào `icore-conf-rank-A-A*.csv`
- assign_ranking.py: output được lưu vào `icore-conf-to-rank.csv`

- openreview_client.py: cung cấp `class OpenReviewClient`
- get_all_venues.py:
  + sử dụng OpenReviewAPI_v1 và v2 để crawl tất cả venues (ko phải submissions) tồn tại trên OpenReview
  + output được lưu vào `venues.json`
- crawl_all_submission.py:
  + sử dụng `class OpenReviewClient`, request conference_notes của các venues trong `venues.json` qua OpenReviewAPI
  + output được lưu vào conference_notes/ folder

- crawl_pdf.py: crawl pdf của các paper trong một conference note
- crawl_pdfs.py: file này dùng để gọi 'crawl_pdf.py' hàng loạt
- check_corrupt_pdf.py: kiểm tra xem có file pdf nào bị corrupt không (optional)
- extract_pdf.py
  + extract các thông tin về text, image, và table của các pdf trong pdfs/
  + output được lưu vào pdfs-extract/
- extract_pdfs.py: file này dùng để gọi 'extract_pdf.py' hàng loạt
- finalize_pdf_extract.py: dùng để tạo ra  pdf-extract-final/

- conference_notes_adjust.py
  + đưa các file `conference_notes/..._v1.json` và `conference_notes/..._v2.json` về cùng format
  + output được lưu vào `conference_notes_adjust/`
  + 735/764
- conference_notes_adjust-extracted.py: dùng để tạo ra conference_notes_adjust-extracted/
- finalize_conference_notes.py: dùng để tạo ra conference_notes_adjust-final/

- crawl citation information từ https://colab.research.google.com/drive/14rgrxcRAAILKXhJNAM-3qBE8lYTEac6s
- merge_citation_text.py: merge papers và citation crawl từ SemanticScholar thành các file JSON, mỗi JSON ứng với một paper
