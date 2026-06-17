import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
GEMINI_FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash-lite")

def generate_readme(metadata, context_string, preferences=None):
    """
    Construct a dynamic prompt honoring wizard preferences and call Gemini.
    """
    if preferences is None:
        preferences = {}

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    theme = preferences.get("theme", "Modern")
    technologies = preferences.get("technologies", [])
    sections = preferences.get("sections", [])
    screenshots = preferences.get("screenshots", [])
    custom_notes = preferences.get("custom_notes", "")

    # Build prompt directives based on wizard choices
    tech_instructions = ""
    if technologies:
        tech_list = ", ".join(technologies)
        tech_instructions = (
            f"- Add standard markdown or Shields.io badges near the top for these technologies: {tech_list}.\n"
        )

    section_instructions = ""
    if sections:
        section_list = "\n".join([f"  * {s}" for s in sections])
        section_instructions = (
            f"- Structure the README around these requested sections:\n{section_list}\n"
        )

    screenshot_instructions = ""
    if screenshots:
        shots_formatted = "\n".join(
            [f"  * ![{s.get('caption', 'Screenshot')}]({s.get('url', '')})" for s in screenshots if s.get("url")]
        )
        if shots_formatted:
            screenshot_instructions = f"- Include these screenshot image links in the Screenshots section:\n{shots_formatted}\n"

    system_instruction = (
        "You are an expert technical documentation engineer. "
        "Your task is to write an exhaustive, production-grade README.md for the provided repository. "
        f"Apply a '{theme}' writing and design style (clean formatting, appropriate spacing, well-structured headers). "
        "Output ONLY raw Markdown without wrapping it in triple backticks (do not start with ```markdown)."
    )

    user_prompt = f"""
Project Details:
- Repository Name: {metadata.get('name')}
- Full Name: {metadata.get('full_name')}
- Description: {metadata.get('description') or 'No description provided.'}
- Primary Language: {metadata.get('language') or 'General'}

Customization Requirements:
{tech_instructions}
{section_instructions}
{screenshot_instructions}
{f"- User Specific Notes: {custom_notes}" if custom_notes else ""}

Codebase Context (Key File Extracts):
{context_string}

Generate the complete README.md now.
"""

    response = None
    models_to_try = [GEMINI_MODEL]
    if GEMINI_FALLBACK_MODEL != GEMINI_MODEL:
        models_to_try.append(GEMINI_FALLBACK_MODEL)

    for model_index, model_name in enumerate(models_to_try):
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.4,
                        max_output_tokens=4000,
                    )
                )
                break
            except Exception as error:
                if "503" not in str(error):
                    raise
                if attempt == 0:
                    time.sleep(2)
                elif model_index == len(models_to_try) - 1:
                    raise
        if response is not None:
            break

    # Clean up any accidental markdown code fences
    output = (getattr(response, "text", None) or "").strip()
    if not output:
        raise RuntimeError("Gemini returned an empty response.")
    if output.startswith("```markdown"):
        output = output[11:]
    elif output.startswith("```"):
        output = output[3:]
    if output.endswith("```"):
        output = output[:-3]

    return output.strip()