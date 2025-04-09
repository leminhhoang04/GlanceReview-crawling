from tqdm import tqdm
import os
import glob
import fitz  # PyMuPDF

pdf_folder = "pdfs"  # Thư mục chứa các file PDF

def is_pdf_corrupt(pdf_path):
    try:
        doc = fitz.open(pdf_path)  # Mở file PDF
        doc.close()
        return False  # Không bị lỗi
    except Exception as e:
        print(f"❌ Lỗi PDF: {pdf_path} - {e}")
        return True  # File bị lỗi

# Kiểm tra toàn bộ file PDF trong thư mục
corrupt_files = []
pdf_glob = glob.glob(os.path.join(pdf_folder, "*/*.pdf"))
print(len(pdf_glob), "file PDF trong thư mục", pdf_folder)
for i, pdf_file in tqdm(enumerate(pdf_glob), total=len(pdf_glob), desc="Kiểm tra file PDF"):
    pdf_path = pdf_file
    if is_pdf_corrupt(pdf_path):
        corrupt_files.append(pdf_file)

# In kết quả
if corrupt_files:
    print("\n📌 Các file PDF bị lỗi:")
    for file in corrupt_files:
        print(f"   - {file}")
else:
    print("✅ Tất cả các file PDF đều hợp lệ!")
