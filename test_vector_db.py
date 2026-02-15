from vector_db import store_document, search_similar, count_documents

# Step 1: Store test documents
store_document(
    "India surpassed Japan to become the fourth-largest economy.",
    "reuters.com"
)

store_document(
    "NASA discovered evidence of water on Mars.",
    "nasa.gov"
)

# Step 2: Print count
print("Total stored documents:", count_documents())

# Step 3: Search
query = "Is India the 4th largest economy?"

results = search_similar(query)

print("\nSearch Results:")
for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
    print("\nContent:", doc)
    print("Source:", metadata["source"])