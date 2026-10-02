from utils.vectorstore import VectorStore
from utils.chunk_expander import expand_neighbors

vector_db = VectorStore.load("vectorstore")

results = [
    {
        "source": "IntroductiontoAgenticAI.pdf",
        "page": 4,
        "chunk_id": 1896,
        "score": 0.7268
    }
]

expanded = expand_neighbors(
    vector_db,
    results,
    before=0,
    after=3
)

for result in expanded:
    print(
        "chunk =", result["chunk_id"],
        "| page =", result["page"],
        "| source =", result["source"],
        "| expanded_from =", result["expanded_from"]
    )