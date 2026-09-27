import json
from pathlib import Path


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "tests"
    / "answer_evaluation_results.json"
)


# ============================================================
# Load benchmark results
# ============================================================

def load_results():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"Results file not found: {RESULTS_FILE}"
        )

    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


# ============================================================
# Citation Evaluation
# ============================================================

def evaluate_citations(result):
    expected_sources = set(
        result.get("expected_sources", [])
    )

    expected_pages = set(
        result.get("expected_pages", [])
    )

    citations = result.get("citations", [])

    if not citations:
        return {
            "source_match": False,
            "page_match": False,
            "citation_present": False,
        }

    cited_sources = {
        citation.get("source")
        for citation in citations
        if citation.get("source")
    }

    cited_pages = {
        citation.get("page")
        for citation in citations
        if citation.get("page") is not None
    }

    source_match = bool(
        expected_sources & cited_sources
    )

    page_match = bool(
        expected_pages & cited_pages
    )

    return {
        "source_match": source_match,
        "page_match": page_match,
        "citation_present": True,
    }

# ============================================================
# Save Evaluation Results
# ============================================================

def save_quality_results(results):
    output_path = (
        PROJECT_ROOT
        / "tests"
        / "citation_evaluation_results.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False,
        )

    return output_path

# ============================================================
# Main
# ============================================================

def main():

    print("=" * 70)
    print("ANSWER QUALITY EVALUATION")
    print("=" * 70)

    results = load_results()

    total = len(results)

    evaluated_results = []

    source_matches = 0
    page_matches = 0
    citations_present = 0

    for index, result in enumerate(
        results,
        start=1,
    ):

        evaluation = evaluate_citations(result)

        if evaluation["source_match"]:
            source_matches += 1

        if evaluation["page_match"]:
            page_matches += 1

        if evaluation["citation_present"]:
            citations_present += 1

        evaluated_result = {
            "question": result["question"],
            "answer": result.get("answer"),
            "context": result.get("context", ""),
            "expected_sources": result.get(
                "expected_sources",
                []
            ),
            "expected_pages": result.get(
                "expected_pages",
                []
            ),
            "citations": result.get(
                "citations",
                []
            ),
            "citation_evaluation": evaluation,

            # These will be filled by the LLM judge later.
            "answer_evaluation": {
                "correctness": None,
                "groundedness": None,
                "completeness": None,
                "hallucination": None,
                "reason": None,
            },
        }

        evaluated_results.append(evaluated_result)

        print(
            f"\n[{index}/{total}] "
            f"{result['question']}"
        )

        print(
            f"  Citation present: "
            f"{evaluation['citation_present']}"
        )

        print(
            f"  Source match: "
            f"{evaluation['source_match']}"
        )

        print(
            f"  Page match: "
            f"{evaluation['page_match']}"
        )

    output_path = save_quality_results(
        evaluated_results
    )

    print("\n" + "=" * 70)
    print("CITATION EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"\nCitation present: "
        f"{citations_present}/{total}"
    )

    print(
        f"Expected source matched: "
        f"{source_matches}/{total}"
    )

    print(
        f"Expected page matched: "
        f"{page_matches}/{total}"
    )

    print(
        f"\nResults saved to:"
    )

    print(output_path)


if __name__ == "__main__":
    main()
