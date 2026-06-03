import requests
from pydantic import BaseModel
from app.chain.runnable import Runnable
from app.utils.config import settings

# förfrågnings basemodel med indata, det som vi skickar till ai
class AskRequest(BaseModel):
    question: str
    stats: dict

# basemodel med svar som skickas till användaren
class AskResponse(BaseModel):
    answer: str

# här byggs prompt med användarens fråga + btv statistik
class PromptBuilder(Runnable[AskRequest, str]):
    name: str = "prompt_builder"

    def invoke(self, data: AskRequest) -> str:
        return f"""Du är en Bitcoin-analytiker. Här är den aktuella statistiken:
- Senaste pris: {data.stats['senaste_pris']} USD
- Payday FOMO-signal: {data.stats['payday_fomo']}
- Bollinger Band-signal: {data.stats['bollinger_signal']}

Användarens fråga: {data.question}

Svara kort, tydligt och på svenska."""

# prompten skickas vidare till openrouter och återkommer tillbaka med svaret
class LLMRunner(Runnable[str, str]):
    name: str = "llm_runner"

    def invoke(self, prompt: str) -> str:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": settings.openrouter_model,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        return response.json()["choices"][0]["message"]["content"]

# här packas svaret från llm i en pydantic modell
class ResponseParser(Runnable[str, AskResponse]):
    name: str = "response_parser"

    def invoke(self, raw: str) -> AskResponse:
        return AskResponse(answer=raw)

# hela kedjan kopplad ihop med | operatorn
ask_pipeline = PromptBuilder() | LLMRunner() | ResponseParser()