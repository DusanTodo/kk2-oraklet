from app.chain.steps import PromptBuilder, AskRequest

# testar att promptbuilder bygger ett prompt med rätt innehåll
def test_prompt_builder_innehåller_frågan():
    builder = PromptBuilder()
    request = AskRequest(
        question="Ska jag köpa Bitcoin nu?",
        stats={
            "senaste_pris": 50000,
            "payday_fomo": "Hög (Lönedags!)",
            "bollinger_signal": "Normal – inom Bollinger-banden"
        }
    )
    result = builder.invoke(request)
    assert "Ska jag köpa Bitcoin nu?" in result
    assert "50000" in result
