import tempfile
import os
import uuid
from pathlib import Path
from typing import List, Dict, Optional

from utils.loader import load_document_pages
from utils.splitter import split_documents
from utils.embeddings import create_embeddings
from utils.vectorstore import VectorStore


def process_document(
    file_content: bytes,
    filename: str,
    vectorstore: VectorStore,
    vectorstore_folder: str
) -> Dict:
    """
    Process a single document and add it to the vectorstore.

    Args:
        file_content: Raw file bytes.
        filename: Original filename.
        vectorstore: The existing VectorStore instance to add to.
        vectorstore_folder: Path to the vectorstore folder for saving.

    Returns:
        Dictionary with document metadata (filename, chunk count, etc.)

    Raises:
        ValueError: If file type is not supported or file is empty.
        RuntimeError: If processing fails.
    """
    # Create temporary file
    suffix = Path(filename).suffix.lower()
    supported = [".pdf", ".docx", ".txt"]
    if suffix not in supported:
        raise ValueError(f"Unsupported file type: {suffix}. Supported: {', '.join(supported)}")

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name

    try:
        # Step 1: Load document pages
        pages = load_document_pages(tmp_path)
        if not pages:
            # Check if it's a PDF - if so, it might be scanned/image-only
            if suffix == ".pdf":
                raise ValueError(
                    "Document contains no extractable text. "
                    "This may be a scanned/image-only PDF. "
                    "Only text-based PDFs, DOCX, and TXT files are supported."
                )
            raise ValueError("Document contains no extractable text.")

        # Override source with original filename in all pages
        for page in pages:
            page["source"] = filename

        # Step 2: Chunk documents
        chunks = split_documents(pages)

        if not chunks:
            raise ValueError("No chunks created from document.")

        # Step 3: Create embeddings
        vectors = create_embeddings(chunks)

        # Step 4: Add to vectorstore
        vectorstore.add_embeddings(vectors, chunks)

        # Step 5: Save updated vectorstore
        vectorstore.save(vectorstore_folder)

        return {
            "filename": filename,
            "document_type": suffix[1:],  # Remove the dot
            "chunks_created": len(chunks),
            "pages_processed": len(pages),
            "status": "processed"
        }

    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def get_document_list(vectorstore: VectorStore) -> List[Dict]:
    """
    Extract document list from vectorstore chunks.

    Returns:
        List of document metadata dictionaries.
    """
    # Group chunks by source filename
    doc_map = {}

    for chunk in vectorstore.chunks:
        source = chunk.get("source", "Unknown")
        if source not in doc_map:
            doc_map[source] = {
                "filename": source,
                "document_type": chunk.get("document_type", "pdf"),
                "chunk_count": 0,
                "pages": set(),
            }
        doc_map[source]["chunk_count"] += 1
        if chunk.get("page"):
            doc_map[source]["pages"].add(chunk["page"])

    # Convert to list
    documents = []
    for doc in doc_map.values():
        documents.append({
            "filename": doc["filename"],
            "document_type": doc["document_type"],
            "chunk_count": doc["chunk_count"],
            "pages": sorted(list(doc["pages"])),
            "status": "processed"
        })

    return documents


def delete_document(filename: str, vectorstore: VectorStore, vectorstore_folder: str) -> Dict:
    """
    Delete a document from the vectorstore by rebuilding the index.

    This is a destructive operation - it removes all chunks with the given source filename
    and rebuilds the FAISS index from scratch.

    Args:
        filename: The source filename to delete.
        vectorstore: The existing VectorStore instance.
        vectorstore_folder: Path to the vectorstore folder for saving.

    Returns:
        Dictionary with deletion result.

    Raises:
        ValueError: If document not found.
        RuntimeError: If deletion fails.
    """
    # Find chunks to keep (not matching the filename)
    chunks_to_keep = [
        chunk for chunk in vectorstore.chunks
        if chunk.get("source") != filename
    ]

    if len(chunks_to_keep) == len(vectorstore.chunks):
        raise ValueError(f"Document not found: {filename}")

    removed_count = len(vectorstore.chunks) - len(chunks_to_keep)

    # Rebuild vectorstore
    new_vectorstore = VectorStore(vectorstore.dimension)

    if chunks_to_keep:
        from utils.embeddings import create_embeddings
        texts = [chunk["text"] for chunk in chunks_to_keep]
        vectors = create_embeddings(chunks_to_keep)
        new_vectorstore.add_embeddings(vectors, chunks_to_keep)

    # Save the rebuilt vectorstore
    new_vectorstore.save(vectorstore_folder)

    # Update the reference
    vectorstore.index = new_vectorstore.index
    vectorstore.chunks = new_vectorstore.chunks

    return {
        "filename": filename,
        "chunks_removed": removed_count,
        "chunks_remaining": len(chunks_to_keep),
        "status": "deleted"
    }