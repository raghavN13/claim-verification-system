from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="India became 4th largest economy"
)

print("Embedding length:", len(response.data[0].embedding))
print("Test successful")