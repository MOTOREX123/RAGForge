from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    pages: list[dict],
    chunk_size: int = 800,
    overlap: int = 150
) -> list[dict]:
    """
    Split page-level documents into smaller chunks
    while preserving metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    chunk_id = 0

    for page in pages:

        text = page["text"]

        page_chunks = splitter.split_text(text)

        for chunk_text in page_chunks:

            chunks.append({
                "text": chunk_text,
                "source": page["source"],
                "page": page["page"],
                "document_type": page.get("document_type", "pdf"),
                "chunk_id": chunk_id
            })

            chunk_id += 1

    return chunks