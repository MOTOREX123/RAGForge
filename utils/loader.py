from pathlib import Path
from pypdf import PdfReader


def load_pdf_pages(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF while preserving useful metadata.

    Returns:
        A list of dictionaries, one for each non-empty page.
    """

    reader = PdfReader(pdf_path)

    pages = []

    source_path = Path(pdf_path)

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if not page_text:
            continue

        page_text = page_text.strip()

        if not page_text:
            continue

        pages.append({
            "text": page_text,
            "page": page_number,
            "source": source_path.name,
            "document_type": "pdf"
        })

    return pages