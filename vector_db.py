import chromadb
from openai import OpenAI
from config import OPENAI_API_KEY, VECTOR_DB_PATH
import uuid

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Chroma persistent client
chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

# Create or load collection
collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)


# Function to generate embedding
def get_embedding(text: str):
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# Function to store text in vector DB
def store_document(text: str, source: str, similarity_threshold=0.90):
    embedding = get_embedding(text)

    # Check if similar document already exists
    results = collection.query(
        query_embeddings=[embedding],
        n_results=1
    )

    if results["documents"] and len(results["documents"][0]) > 0:
        distance = results["distances"][0][0]

        similarity = 1 - distance

        if similarity >= similarity_threshold:
            print("Duplicate detected. Skipping storage.")
            return False

    # Store new document
    doc_id = str(uuid.uuid4())

    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[{"source": source}],
        ids=[doc_id]
    )

    print(f"Stored new document: {doc_id}")

    return True


# Function to search similar documents
def search_similar(query: str, n_results=5, similarity_threshold=0.75):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    filtered_documents = []
    filtered_metadatas = []

    if results["documents"]:

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, metadata, distance in zip(documents, metadatas, distances):

            similarity = 1 - distance

            if similarity >= similarity_threshold:
                filtered_documents.append(doc)
                filtered_metadatas.append(metadata)

    return {
        "documents": [filtered_documents],
        "metadatas": [filtered_metadatas]
    }


# Function to check number of stored documents
def count_documents():
    return collection.count()