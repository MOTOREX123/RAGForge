from utils.web_search import web_search


question = "What is the latest stable version of Python?"


result = web_search(question)


print("\nANSWER")
print("=" * 60)

print(result["answer"])


print("\nSEARCH QUERIES")
print("=" * 60)

for query in result["search_queries"]:
    print(query)


print("\nSOURCES")
print("=" * 60)

for i, source in enumerate(result["sources"], start=1):

    print(f"\n{i}. {source['title']}")
    print(f"   {source['url']}")