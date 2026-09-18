from pathlib import Path

from utils.loader import load_pdf_pages
from utils.splitter import split_documents


project_root = Path(__file__).resolve().parents[1]

pdf_path = project_root / "data" / "AI & ML DIGITAL NOTES.pdf"

pages = load_pdf_pages(str(pdf_path))

chunks = split_documents(pages)

print(f"Total pages: {len(pages)}")
print(f"Total chunks: {len(chunks)}")

print("\nFirst chunk:")
print(chunks[0])