import faiss
import numpy as np
import json
from pathlib import Path


class VectorStore:

    def __init__(self, dimension: int):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(dimension)

        self.chunks = []

    # ---------------------------------------------------------
    # ADD EMBEDDINGS
    # ---------------------------------------------------------

    def add_embeddings(self, embeddings, chunks):

        embeddings = np.array(
            embeddings,
            dtype="float32"
        )

        # Normalize vectors so inner product becomes
        # cosine similarity.
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

        self.chunks.extend(chunks)

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    def search(self, query_embedding, k=5):

        query_embedding = np.array(
            [query_embedding],
            dtype="float32"
        )

        faiss.normalize_L2(query_embedding)

        similarities, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for similarity, idx in zip(
            similarities[0],
            indices[0]
        ):

            if idx != -1:

                results.append({
                    "text": self.chunks[idx]["text"],
                    "source": self.chunks[idx]["source"],
                    "page": self.chunks[idx]["page"],
                    "chunk_id": self.chunks[idx]["chunk_id"],
                    "score": float(similarity)
                })

        return results

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    def save(self, folder="vectorstore"):

        folder = Path(folder)

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        # Save FAISS index
        faiss.write_index(
            self.index,
            str(folder / "index.faiss")
        )

        # Save chunk metadata
        with open(
            folder / "chunks.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.chunks,
                f,
                ensure_ascii=False,
                indent=2
            )

        print("Vector store saved successfully!")

    # ---------------------------------------------------------
    # LOAD
    # ---------------------------------------------------------

    @classmethod
    def load(cls, folder="vectorstore"):

        folder = Path(folder)

        index_path = folder / "index.faiss"
        chunks_path = folder / "chunks.json"

        if not index_path.exists():
            raise FileNotFoundError(
                "FAISS index not found."
            )

        if not chunks_path.exists():
            raise FileNotFoundError(
                "Chunk metadata not found."
            )

        # Load FAISS index
        index = faiss.read_index(
            str(index_path)
        )

        # Load chunks
        with open(
            chunks_path,
            "r",
            encoding="utf-8"
        ) as f:

            chunks = json.load(f)

        vector_store = cls(
            index.d
        )

        vector_store.index = index

        vector_store.chunks = chunks

        return vector_store