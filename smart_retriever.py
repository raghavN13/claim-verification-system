from claim_classifier import classify_claim
from hybrid_retriever import hybrid_retrieve
from vector_db import search_similar


def smart_retrieve(claim: str):

    classification = classify_claim(claim)

    claim_type = classification["type"]
    volatility = classification["volatility"]

    print(f"Claim type: {claim_type}")
    print(f"Volatility: {volatility}")

    vector_results = search_similar(claim, n_results=3)

    cache_hit = False

    if vector_results["documents"] and vector_results["documents"][0]:
        cache_hit = True

    # Decision logic
    if claim_type == "historical" and cache_hit:

        print("Using cache (historical claim)")
        return vector_results, classification, "CACHE_HIT"

    elif volatility == "low" and cache_hit:

        print("Using cache (low volatility)")
        return vector_results, classification, "CACHE_HIT"

    elif volatility == "medium":

        print("Hybrid retrieval (medium volatility)")
        evidence = hybrid_retrieve(claim)
        return evidence, classification, "HYBRID"

    else:

        print("Full web retrieval (high volatility)")
        evidence = hybrid_retrieve(claim)
        return evidence, classification, "WEB"