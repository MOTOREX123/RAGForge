from pathlib import Path
from pypdf import PdfReader
from typing import List, Dict


def load_pdf_pages(pdf_path: str) -> List[Dict]:
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


def load_docx_pages(docx_path: str) -> List[Dict]:
    """
    Extract text from a DOCX file.

    Returns:
        A list of dictionaries, one per document (DOCX doesn't have clear page boundaries).
    """
    try:
        from docx import Document
    except ImportError:
        raise ImportError("python-docx is required for DOCX support. Install with: pip install python-docx")

    doc = Document(docx_path)
    source_path = Path(docx_path)

    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())

    if not full_text:
        return []

    combined_text = "\n\n".join(full_text)

    return [{
        "text": combined_text,
        "page": 1,
        "source": source_path.name,
        "document_type": "docx"
    }]


def load_txt_pages(txt_path: str) -> List[Dict]:
    """
    Extract text from a TXT file.

    Returns:
        A list of dictionaries, one per document.
    """
    source_path = Path(txt_path)

    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        return []

    return [{
        "text": text,
        "page": 1,
        "source": source_path.name,
        "document_type": "txt"
    }]


def load_document_pages(file_path: str) -> List[Dict]:
    """
    Load document pages based on file extension.

    Args:
        file_path: Path to the document file.

    Returns:
        List of page dictionaries with text and metadata.

    Raises:
        ValueError: If file extension is not supported.
    """
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return load_pdf_pages(file_path)
    elif suffix == ".docx":
        return load_docx_pages(file_path)
    elif suffix == ".txt":
        return load_txt_pages(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Supported: .pdf, .docx, .txt")


def get_supported_extensions() -> List[str]:
    """Return list of supported file extensions."""
    return [".pdf", ".docx", ".txt"]