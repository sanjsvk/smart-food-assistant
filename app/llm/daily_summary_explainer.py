from app.config import MOCK_LLM
from openai import OpenAI, OpenAIError, APITimeoutError

client = OpenAI()

def explain_daily_summary(summary):
    fallback = (
        f"Today you logged {summary['meal_count']} meals. "
        f"You consumed {summary['intake']['calories']} calories "
        f"and {summary['intake']['protein']}g protein."
    )

    if MOCK_LLM:
        return fallback

    prompt = (
        "You are a concise nutrition assistant.\n\n"
        "Summarize today's eating in 2–3 sentences.\n"
        "Focus on goal progress and patterns.\n\n"
        f"Summary data:\n{summary}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            timeout=30
        )
        return response.choices[0].message.content.strip()

    except (APITimeoutError, OpenAIError, Exception):
        return fallback