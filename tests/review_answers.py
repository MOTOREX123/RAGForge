import json
from pathlib import Path

INPUT_FILE = Path("tests/answer_evaluation_results.json")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    results = json.load(f)

print("=" * 80)
print("RAGFORGE ANSWER REVIEW")
print("=" * 80)

for i, result in enumerate(results, start=1):
    print(f"\n{'=' * 80}")
    print(f"QUESTION {i}/28")
    print("=" * 80)

    print(f"\nQuestion:")
    print(result.get("question", ""))

    print(f"\nAnswer:")
    print(result.get("answer", ""))

    print(f"\nExpected source:")
    print(", ".join(result.get("expected_sources", [])))

    print(f"Expected pages:")
    print(result.get("expected_pages", []))

    print(f"\nCitations:")
    for citation in result.get("citations", []):
        print(
            f"  [{citation.get('id')}] "
            f"{citation.get('source')} "
            f"(page {citation.get('page')})"
        )

print("\n" + "=" * 80)
print("REVIEW COMPLETE")
print("=" * 80)