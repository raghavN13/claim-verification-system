from tavily import TavilyClient
from config import TAVILY_API_KEY
import time

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query: str, max_results=3, retries=2):

    for attempt in range(retries):

        try:
            response = tavily_client.search(
                query=query,
                max_results=max_results
            )

            evidence_list = []

            for result in response["results"]:
                evidence = {
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", "")
                }

                evidence_list.append(evidence)

            return evidence_list

        except Exception as e:

            print(f"Tavily timeout (attempt {attempt+1}/{retries})")

            if attempt < retries - 1:
                time.sleep(2)
            else:
                print("Web search failed. Using existing knowledge base.")
                return []