from web_search import search_web
from vector_db import store_document


def ingest_from_web(query: str):

    print(f"\nSearching web for: {query}")

    results = search_web(query)

    stored_count = 0

    for result in results:

        content = result["content"]
        url = result["url"]

        if content and len(content) > 50:

            stored = store_document(content, url)

            if stored:
                stored_count += 1

    print(f"\nStored {stored_count} new documents")

    return results