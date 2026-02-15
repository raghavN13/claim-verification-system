from openai import OpenAI
from config import OPENAI_API_KEY
from smart_retriever import smart_retrieve
client = OpenAI(api_key=OPENAI_API_KEY)


def format_evidence(results):
    evidence_list = []

    if not results["documents"]:
        return ""

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    for doc, metadata in zip(docs, metadatas):
        evidence = f"""
Source: {metadata.get('source', 'Unknown')}
Content: {doc}
"""
        evidence_list.append(evidence)

    return "\n".join(evidence_list)


def verify_claim(claim: str):

    print(f"\nVerifying claim: {claim}")

    evidence_result, classification, retrieval_mode = smart_retrieve(claim)

    evidence_text = ""

    if isinstance(evidence_result, dict):

        docs = evidence_result["documents"][0]
        metadatas = evidence_result["metadatas"][0]

        for doc, metadata in zip(docs, metadatas):

            evidence_text += f"""
Source: {metadata.get('source')}
Content: {doc}
"""

    else:

        for evidence in evidence_result:

            evidence_text += f"""
Source: {evidence['source']}
Content: {evidence['content']}
"""

    prompt = f"""
You are a professional fact-checking assistant.

Claim:
{claim}

Claim Type: {classification['type']}
Volatility: {classification['volatility']}
Retrieval Mode: {retrieval_mode}

Evidence:
{evidence_text}

Return:

Verdict: TRUE / FALSE / PARTIALLY TRUE / NOT ENOUGH EVIDENCE

Confidence: percentage

Explanation:

Citations:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0
    )

    return response.choices[0].message.content