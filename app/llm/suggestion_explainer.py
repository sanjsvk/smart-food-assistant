from openai import OpenAI, OpenAIError, APITimeoutError
from app.config import MOCK_LLM

client = OpenAI()


def explain_suggestions(remaining, suggestions):
    """
    Returns a concise natural-language explanation for why the suggested foods
    fit within the user's remaining calorie and protein budget.

    This function must NEVER affect which foods are suggested.
    It is strictly a narration layer.
    """

    fallback_text = (
        f"You have {remaining['calories']} calories and "
        f"{remaining['protein']}g protein remaining today. "
        "These food options fit well within your goals and help balance "
        "protein intake without overshooting calories."
    )

    # Development / offline mode
    if MOCK_LLM:
        return fallback_text

    # Build concise, constrained prompt
    prompt = (
        "You are a concise nutrition assistant.\n\n"
        "Explain why the following food suggestions fit within the user's "
        "remaining nutrition budget.\n\n"
        "Rules:\n"
        "- Respond in ONE short paragraph.\n"
        "- Maximum 3–4 sentences.\n"
        "- Do NOT explain each food individually.\n"
        "- Focus on overall reasoning (protein density, calorie efficiency).\n"
        "- Do NOT repeat numeric lists unless absolutely necessary.\n\n"
        f"Remaining calories: {remaining['calories']}\n"
        f"Remaining protein: {remaining['protein']}g\n\n"
        "Suggested foods:\n"
    )

    for food in suggestions:
        prompt += f"- {food['name']}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            timeout=30
        )

        return response.choices[0].message.content.strip()

    except (APITimeoutError, OpenAIError, Exception):
        # Fail safely — never break the suggestions endpoint
        return fallback_text