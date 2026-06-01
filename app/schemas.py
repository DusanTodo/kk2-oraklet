from pydantic import BaseModel
from typing import Dict, Any

# det data som vi ska skicka in genom fast api
class QueryInput(BaseModel):
    question: str

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