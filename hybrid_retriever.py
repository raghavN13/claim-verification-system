from vector_db import search_similar, store_document
from web_search import search_web


def hybrid_retrieve(claim, vector_limit=3, web_limit=3):

    combined_evidence = []

    # Step 1: Retrieve from vector DB
    vector_results = search_similar(claim, n_results=vector_limit)

    if vector_results["documents"]:

        docs = vector_results["documents"][0]
        metadatas = vector_results["metadatas"][0]

        for doc, metadata in zip(docs, metadatas):

            combined_evidence.append({
                "content": doc,
                "source": metadata.get("source", "vector_db"),
                "type": "vector_db"
            })

    # Step 2: Retrieve from web
    web_results = search_web(claim, max_results=web_limit)

    for result in web_results:

        content = result["content"]
        url = result["url"]

        if content and len(content) > 50:

            # store in vector DB for future reuse
            store_document(content, url)

            combined_evidence.append({
                "content": content,
                "source": url,
                "type": "web"
            })

    # Step 3: Remove duplicates
    seen = set()
    unique_evidence = []

    for evidence in combined_evidence:

        content_hash = hash(evidence["content"])

        if content_hash not in seen:

            seen.add(content_hash)
            unique_evidence.append(evidence)

    return unique_evidence