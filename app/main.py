from fastapi import FastAPI

app = FastAPI(
    title="KK2 – Oraklet",
    description="REST-API som kombinerar pandas dataanalys med en avancerad LLM via OpenRouter",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}