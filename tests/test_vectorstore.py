from pathlib import Path

from utils.loader import load_pdf_pages
from utils.splitter import split_documents
from utils.embeddings import create_embeddings
from utils.vectorstore import VectorStore


# Project root
project_root = Path(__file__).resolve().parents[1]

# PDF
pdf_path = project_root / "data" / "AI & ML DIGITAL NOTES.pdf"

# -----------------------------------------
# STEP 1: Load PDF
# -----------------------------------------

pages = load_pdf_pages(str(pdf_path))

print(f"Pages loaded: {len(pages)}")


# -----------------------------------------
# STEP 2: Split
# -----------------------------------------

chunks = split_documents(pages)

print(f"Chunks created: {len(chunks)}")


# -----------------------------------------
# STEP 3: Create embeddings
# -----------------------------------------

vectors = create_embeddings(chunks)

print(f"Embeddings created: {len(vectors)}")
print(f"Embedding dimension: {len(vectors[0])}")


# -----------------------------------------
# STEP 4: Create VectorStore
# -----------------------------------------

vector_store = VectorStore(len(vectors[0]))

vector_store.add_embeddings(
    vectors,
    chunks
)

print(f"Stored chunks: {len(vector_store.chunks)}")


# -----------------------------------------
# STEP 5: Save
# -----------------------------------------

vectorstore_path = project_root / "vectorstore"

vector_store.save(str(vectorstore_path))


# -----------------------------------------
# STEP 6: Load again
# -----------------------------------------

loaded_store = VectorStore.load(str(vectorstore_path))

print("\nVectorStore loaded successfully!")

print(f"Loaded chunks: {len(loaded_store.chunks)}")
print(f"Loaded dimension: {loaded_store.dimension}")


# -----------------------------------------
# STEP 7: Verify
# -----------------------------------------

assert len(loaded_store.chunks) == len(chunks)

assert loaded_store.dimension == len(vectors[0])

print("\n✅ SAVE + LOAD TEST PASSED!")