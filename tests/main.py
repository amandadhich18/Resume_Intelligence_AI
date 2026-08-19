import pymupdf

from src.text_cleaner import clean_text
from src.chunker import create_chunks


pdf_path = "Data/Resume/Aman_Dadhich_Resume.pdf"

document = pymupdf.open(pdf_path)

all_text = ""

for page in document:
    all_text += page.get_text() + "\n"

document.close()

cleaned_text = clean_text(all_text)

chunks = create_chunks(
    cleaned_text,
    chunk_size=500,
    overlap=100
)

print(f"===== TOTAL CHUNKS: {len(chunks)} =====\n")

for index, chunk in enumerate(chunks):
    print(f"--- CHUNK {index + 1} ---")
    print(chunk)
    print("\n")