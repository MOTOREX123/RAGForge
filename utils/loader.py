from pathlib import Path
from pypdf import PdfReader
from typing import List, Dict
import tempfile
import os

try:
    import pypdfium2 as pdfium
    PYPODFIUM2_AVAILABLE = True
except ImportError:
    PYPODFIUM2_AVAILABLE = False

# Global PaddleOCR instance (lazy-loaded)
_paddleocr_instance = None


def _get_paddleocr():
    """Lazy-load PaddleOCR instance."""
    global _paddleocr_instance
    if _paddleocr_instance is None:
        # Disable model source check and oneDNN for better compatibility
        os.environ.setdefault('PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK', 'True')
        os.environ.setdefault('PADDLE_DISABLE_ONEDNN', '1')
        from paddleocr import PaddleOCR
        _paddleocr_instance = PaddleOCR(use_textline_orientation=True, lang='en', enable_mkldnn=False)
    return _paddleocr_instance


def _ocr_pdf_page(pdf_path: str, page_number: int) -> str:
    """
    Render a PDF page to image and run PaddleOCR.
    
    Args:
        pdf_path: Path to the PDF file.
        page_number: 1-based page number.
    
    Returns:
        Extracted text from OCR, or empty string if OCR fails.
    """
    if not PYPODFIUM2_AVAILABLE:
        return ""
    
    temp_image_path = None
    try:
        pdf = pdfium.PdfDocument(pdf_path)
        page = pdf[page_number - 1]  # 0-based index
        
        # Render at 150 DPI for faster OCR on CPU
        bitmap = page.render(scale=150/72)
        pil_image = bitmap.to_pil()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            temp_image_path = tmp.name
            pil_image.save(temp_image_path)
        
        # Run OCR
        ocr = _get_paddleocr()
        result = ocr.predict(temp_image_path)
        
        # Extract text from result (OCRResult is dict-like)
        texts = []
        if result and len(result) > 0:
            res = result[0]
            if isinstance(res, dict) or hasattr(res, 'keys'):
                # Dict-style access for OCRResult
                rec_texts = res.get('rec_texts', []) if hasattr(res, 'get') else res['rec_texts']
                if rec_texts:
                    texts.extend(rec_texts)
        
        return "\n".join(texts)
    
    except Exception as e:
        print(f"[LOADER] OCR failed for page {page_number}: {e}")
        return ""
    finally:
        # Clean up temp image
        if temp_image_path and os.path.exists(temp_image_path):
            try:
                os.unlink(temp_image_path)
            except:
                pass


def load_pdf_pages(pdf_path: str) -> List[Dict]:
    """
    Extract text from a PDF while preserving useful metadata.
    Falls back to PaddleOCR for scanned/image-only pages.

    Returns:
        A list of dictionaries, one for each non-empty page.
    """

    reader = PdfReader(pdf_path)

    pages = []

    source_path = Path(pdf_path)

    # First pass: try normal text extraction
    total_text_length = 0
    extracted_pages = []
    
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if not page_text:
            extracted_pages.append((page_number, ""))
            continue

        page_text = page_text.strip()

        if not page_text:
            extracted_pages.append((page_number, ""))
            continue

        total_text_length += len(page_text)
        extracted_pages.append((page_number, page_text))

    # Check if we have sufficient text overall
    # Threshold: at least 100 characters total, or at least 1 page with text
    has_sufficient_text = total_text_length >= 100 or any(text for _, text in extracted_pages if text)
    
    if has_sufficient_text:
        print(f"[LOADER] PDF text extraction: {total_text_length} characters from {len([p for p in extracted_pages if p[1]])} pages")
        for page_number, page_text in extracted_pages:
            if page_text:
                pages.append({
                    "text": page_text,
                    "page": page_number,
                    "source": source_path.name,
                    "document_type": "pdf"
                })
        return pages

    # Fallback: Use PaddleOCR for scanned/image-only PDF
    print(f"[LOADER] PDF text extraction: {total_text_length} characters - insufficient, starting PaddleOCR fallback")
    
    if not PYPODFIUM2_AVAILABLE:
        print("[LOADER] pypdfium2 not available, cannot render PDF for OCR")
        return pages
    
    try:
        ocr = _get_paddleocr()
    except Exception as e:
        print(f"[LOADER] Failed to initialize PaddleOCR: {e}")
        return pages

    ocr_pages = []
    for page_number, page_text in extracted_pages:
        if page_text:
            # Page already has text, use it
            ocr_pages.append({
                "text": page_text,
                "page": page_number,
                "source": source_path.name,
                "document_type": "pdf"
            })
        else:
            # Page has no text, run OCR
            print(f"[LOADER] OCR page {page_number}/{len(extracted_pages)}")
            ocr_text = _ocr_pdf_page(pdf_path, page_number)
            if ocr_text and ocr_text.strip():
                ocr_pages.append({
                    "text": ocr_text.strip(),
                    "page": page_number,
                    "source": source_path.name,
                    "document_type": "pdf"
                })
                print(f"[LOADER] OCR page {page_number}: extracted {len(ocr_text)} characters")
            else:
                print(f"[LOADER] OCR page {page_number}: no text extracted")

    total_ocr_chars = sum(len(p["text"]) for p in ocr_pages)
    print(f"[LOADER] PaddleOCR extracted {total_ocr_chars} characters from {len(ocr_pages)} pages")
    
    return ocr_pages


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