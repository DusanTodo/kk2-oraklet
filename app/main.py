import io
import pandas as pd
from app.data import btc_data
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.chain.steps import AskRequest
from app.chain.pipeline import ask_pipeline
from app.utils.config import settings
from app.schemas import QueryInput, FinalResponse

# fastapi app creation
app = FastAPI(
    title="KK2 – Oraklet",
    description="REST-API som kombinerar pandas dataanalys med en avancerad LLM via OpenRouter",
    version="1.0.0"
)

# lagrar csv datasetet direkt i minnet
uploaded_df: pd.DataFrame | None = None

# enkelt status check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# laddar upp CSV-fil och returnera metadata
@app.post("/data/upload")
async def upload_csv(file: UploadFile = File(...)):
    global uploaded_df

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Endast CSV-filer är tillåtna")

    contents = await file.read()
    uploaded_df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    return {
        "rows": len(uploaded_df),
        "columns": list(uploaded_df.columns),
        "dtypes": {col: str(dtype) for col, dtype in uploaded_df.dtypes.items()}
    }

# returnerar beskrivande statistik från uppladdad CSV
@app.get("/data/stats")
def get_stats():
    global uploaded_df

    if uploaded_df is None:
        raise HTTPException(status_code=404, detail="Inget dataset har laddats upp än")

    return uploaded_df.describe().to_dict()

# fråga LLM om datat
@app.post("/ai/ask", response_model=FinalResponse)
def ask(request: QueryInput):
    if uploaded_df is None:
        raise HTTPException(status_code=400, detail="Ladda upp ett dataset först via /data/upload")

    stats = btc_data.get_stats()
    enriched_request = AskRequest(question=request.question, stats=stats)

    result = ask_pipeline.invoke(enriched_request)
    return FinalResponse(
    question=request.question,
    answer=result.answer,
    model=settings.openrouter_model
)