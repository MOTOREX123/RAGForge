from pathlib import Path

from utils.loader import load_pdf_pages


project_root = Path(__file__).resolve().parents[1]

pdf_path = project_root / "data" / "AI & ML DIGITAL NOTES.pdf"

pages = load_pdf_pages(str(pdf_path))

print(f"Total pages: {len(pages)}")

print("\nFirst page metadata:")
print(pages[0])