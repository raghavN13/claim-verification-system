from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)


def classify_claim(claim: str):

    prompt = f"""
You are a claim classification engine.

Classify the following claim into:

1. type:
   - historical (never changes)
   - current (recent but stable)
   - breaking (fast-changing news)
   - general (generic claim)

2. volatility:
   - low
   - medium
   - high

Return JSON only:

{{
  "type": "...",
  "volatility": "..."
}}

Claim:
{claim}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0
    )

    try:
        result = json.loads(response.choices[0].message.content)
        return result
    except:
        return {
            "type": "general",
            "volatility": "medium"
        }