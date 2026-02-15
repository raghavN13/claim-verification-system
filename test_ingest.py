from ingest import ingest_from_web
from vector_db import count_documents

query = "India became 4th largest economy"

print("Documents before:", count_documents())

ingest_from_web(query)

print("Documents after:", count_documents())