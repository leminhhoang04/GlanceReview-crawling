import os
import json
import base64
from PyPDF2 import PdfReader
import pdfplumber
import fitz  # pymupdf
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

os.makedirs('pdfs-extract', exist_ok=True)

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        try:
            content = page.extract_text()
            if content:
                text += content + "\n"
        except:
            pass
    return text

def extract_images(pdf_path, output_folder="pdfs-extract-image"):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_list = []
    
    for page_index in range(len(doc)):
        try:
            page = doc[page_index]
            images = page.get_images(full=False)
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = f"{output_folder}/page{page_index+1}_img{img_index+1}.{image_ext}"
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_bytes)

                image_info = {
                    "page": page_index + 1,
                    "image_index": img_index + 1,
                    "file_path": image_filename,
                }
                image_list.append(image_info)
        except:
            pass
    
    return image_list

def extract_tables(pdf_path):
    tables_data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                try:
                    tables = page.extract_tables()
                    
                    for table_index, table in enumerate(tables):
                        tables_data.append({
                            "page": page_number,
                            "table_index": table_index + 1,
                            "data": table
                        })
                except:
                    pass
    except:
        pass
                    
    return tables_data

def extract_pdf_info(pdf_path):
    pdfname = pdf_path.split('/')[-1][:-4]
    output_image_folder = f'pdfs-extract-image/{pdfname}'
    os.makedirs(output_image_folder, exist_ok=True)

    extracted_data = {
        "file_path": pdf_path,
        "text": extract_text(pdf_path),
        "images": extract_images(pdf_path, output_image_folder),
        "tables": extract_tables(pdf_path)
    }
    return extracted_data

def process_pdf(pdf_name):
    pdf_local_path = f'pdfs/{pdf_name}'
    pdfname = pdf_name[:-4]
    result = extract_pdf_info(pdf_local_path)

    if len(result["text"]) > 0:
        # Xuất ra file JSON
        output_json_path = f"pdfs-extract/{pdfname}.json"
        with open(output_json_path, "w", encoding="utf-8", errors="replace") as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)
        




pdf_folder = 'pdfs/'
pdf_list = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
num_workers = 32

with Pool(processes=num_workers) as pool:
    # tqdm kết hợp với pool.imap để theo dõi tiến trình
    results = list(tqdm(pool.imap(process_pdf, pdf_list),
                        total=len(pdf_list),
                        desc="🔨 Processing PDFs", 
                        unit="file", 
                        ncols=100))

print("\n✅ All PDFs processed!")