from pathlib import Path

from utils.loader import load_pdf_pages
from utils.splitter import split_documents
from utils.embeddings import create_embeddings
from utils.vectorstore import VectorStore


def main():

    # ==========================================
    # PROJECT PATH
    # ==========================================

    project_root = Path(__file__).resolve().parent

    data_folder = project_root / "data"

    vectorstore_folder = project_root / "vectorstore"


    # ==========================================
    # FIND PDF DOCUMENTS
    # ==========================================

    pdf_paths = list(data_folder.glob("*.pdf"))

    print("=" * 60)
    print("DOCUMENT INGESTION")
    print("=" * 60)

    print(f"Found {len(pdf_paths)} PDF document(s).")


    if not pdf_paths:
        print("No PDF documents found in the data folder.")
        return


    # ==========================================
    # STEP 1: LOAD DOCUMENTS
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 1 : Loading PDF Documents")
    print("=" * 60)

    all_pages = []

    for pdf_path in pdf_paths:

        print(f"\nLoading: {pdf_path.name}")

        pages = load_pdf_pages(str(pdf_path))

        print(f"Pages loaded: {len(pages)}")

        all_pages.extend(pages)


    print(f"\nTotal Pages: {len(all_pages)}")


    # ==========================================
    # STEP 2: CHUNKING
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 2 : Chunking")
    print("=" * 60)

    chunks = split_documents(all_pages)

    print(f"Total Chunks: {len(chunks)}")


    # ==========================================
    # STEP 3: EMBEDDINGS
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 3 : Creating Embeddings")
    print("=" * 60)

    vectors = create_embeddings(chunks)

    print(f"Total Embeddings: {len(vectors)}")
    print(f"Embedding Dimension: {len(vectors[0])}")


    # ==========================================
    # STEP 4: CREATE VECTOR STORE
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 4 : Creating FAISS Vector Store")
    print("=" * 60)

    vector_store = VectorStore(len(vectors[0]))

    vector_store.add_embeddings(
        vectors,
        chunks
    )

    print("FAISS index created successfully!")
    print(f"Total Stored Chunks: {len(vector_store.chunks)}")


    # ==========================================
    # STEP 5: SAVE VECTOR STORE
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 5 : Saving Vector Store")
    print("=" * 60)

    vector_store.save(str(vectorstore_folder))

    print(f"Vector store saved to: {vectorstore_folder}")


    # ==========================================
    # DONE
    # ==========================================

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()