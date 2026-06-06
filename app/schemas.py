from pydantic import BaseModel, Field
from typing import Dict, Any

# det data som vi ska skicka in genom fast api
class QueryInput(BaseModel):
    question: str = Field(default=..., examples=["Ska jag köpa Bitcoin nu?"])

# data som vi ska skicka in inne i prompt builder
class PromptInput(BaseModel):
    question: str
    stats_dict: Dict[str, Any]

# data som skall skickas från prmpt builder till llm i vårt fall openrouter omdel
class LLMInput(BaseModel):
    full_prompt: str

# data som kommer tillbaka från ai model
class LLMOutput(BaseModel):
    raw_text: str

# final svare som skickas till oss
class FinalResponse(BaseModel):
    question: str
    answer: str
    model: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "Ska jag köpa Bitcoin nu?",
                "answer": "BTC handlas vid 67 432 USD. Bollinger signalen säger KÖP – priset rör vid nedre bandet. Payday FOMO är hög.",
                "model": "openai/gpt-5.4-mini"
            }
        }
    }