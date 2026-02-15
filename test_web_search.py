from web_search import search_web

query = "India became 4th largest economy"

results = search_web(query)

print("\nWeb Search Results:\n")

for i, result in enumerate(results):
    print(f"Result {i+1}")
    print("Title:", result["title"])
    print("URL:", result["url"])
    print("Content:", result["content"])
    print("-" * 50)