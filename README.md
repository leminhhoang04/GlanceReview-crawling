# Crawling

Crawl conference notes:
```python
python get_all_venues.py
python crawl_all_submission.py
```

Crawl icore data and assign ranking for conference notes:
```python
python get_icore_conference_rank.py
python get_icore_conference_rank_filter.py (optional, to filter A/A* conferences)
python assign_ranking.py
```

Download all papers and extract data:
```python
python crawl_pdfs.py
python extract_pdfs.py
python finalize_pdf_extract.py
```

Since the JSON format of OpenReview API v1 and API v2 are difference, we need to create a common format:
```python
python conference_notes_adjust.py
python conference_notes_adjust-extracted.py
python finalize_conference_notes.py
```

We crawl citation information of papers using [Google Colab Notebook](https://colab.research.google.com/drive/14rgrxcRAAILKXhJNAM-3qBE8lYTEac6s)

Finally, merge all information of each paper into a JSON file:
```python
python merge_citation_text.py
```

# Result

Each processed file from the process_data is a dictionary with key as the id of the paper and value as a dictionary in the form of:
```python
{
    "id": "unique_id",
    "content": {
        "title": {"value": "Title"}
        "abstract": {"value": "Abstract"}
        "authors": {"value": ["Author1", "Author2"]},
        "keywords": {"value": ["keyword1", "keyword2"]},
        "TLDR": {"value": "TLDR"},
        "pdf-public": {"value": "url to pdf"},
        "is_accepted": {"value": true/false},
    }
    "text": "Full text of the paper",
    "references": "Text of references",
    "appendix": "Text of appendix",
    "semanticsholar_id": "Semantic Scholar ID",
    "citation_count": 10,
    "conference_name": "Conference Name",
    "acronym": "Conference Acronym",
    "year": 2023,
    "rank": "A*"
}
```