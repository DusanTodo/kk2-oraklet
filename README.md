# KK2 ORAKLET

FastAPI-projekt som laddar upp CSV-data, visar statistik och låter användaren ställa frågor till en LLM via en typad Runnable-kedja.

## Starta projektet

```bash
uv sync
uv run uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `POST /data/upload`
- `GET /data/stats`
- `POST /ai/ask`

## Exempel

Ladda upp CSV:

```bash
curl -X POST "http://127.0.0.1:8000/data/upload" -F "file=@data/btcusd-daily.csv"
```

Ställ en fråga:

```bash
curl -X POST "http://127.0.0.1:8000/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Ska jag köpa Bitcoin nu?"}'
```

## Tester

```bash
uv run pytest app/tests/ -v
```

## Konfiguration

Projektet använder `.env` för känsliga värden och konfiguration via `pydantic_settings`.
`.env` ska inte checkas in i Git.

## AI-flöde

Endpointen `/ai/ask` använder en typad Runnable-kedja:
`PromptBuilder | LLMRunner | ResponseParser`

## Övrigt

Testerna täcker både endpoints och kedjan, bland annat health, giltig CSV, ogiltig filtyp, stats utan uppladdad data och att PromptBuilder bygger rätt prompt.

Projektet sparar dataset i minnet under körning och är gjort för utbildningssyfte, inte produktion.
