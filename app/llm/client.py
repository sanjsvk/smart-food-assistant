import json
from openai import OpenAI
from app.llm.prompts import FOOD_PARSING_PROMPT
from app.config import OPENAI_API_KEY, MOCK_LLM

client = OpenAI(api_key=OPENAI_API_KEY)

class LLMParseError(Exception):
    pass


def parse_food_input(user_input: str, context: list | None = None) -> dict:
    if MOCK_LLM:
        # Deterministic mock output for development
        text = user_input.lower()

        items = []

        if "egg" in text:
            items.append({
                "name": "egg",
                "quantity": 2 if "2" in text else 1,
                "unit": "item"
            })

        if "apple" in text:
            items.append({
                "name": "apple",
                "quantity": 1,
                "unit": "item"
            })

        return {
            "items": items,
            "confidence": 0.95
        }

    # ---- Real LLM path (disabled for now) ----
    prompt = FOOD_PARSING_PROMPT.format(user_input=user_input)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        timeout=10
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise LLMParseError(f"Invalid JSON from LLM: {content}")