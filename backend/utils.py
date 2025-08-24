import json
from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    dream_text: str = Field(..., min_length=20, description="Raw dream notes")
    constraints: str | None = Field(default=None, description="Optional guidance: genre, tone, ending, rating, etc.")
    model: str = Field(default="gemini-1.5-flash",
                       description="Gemini model name, e.g., gemini-1.5-flash or gemini-1.5-pro")

class ScreenplayPackage(BaseModel):
    logline: str
    genre: str
    themes: list[str]
    characters: list[dict]
    settings: list[str]
    beat_sheet: list[dict]
    fountain: str


def parse_llm_json(text: str) -> ScreenplayPackage:
    """Attempt strict JSON parse with a soft fallback."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            data = json.loads(text[start:end + 1])
        else:
            raise
    return ScreenplayPackage(**data)


