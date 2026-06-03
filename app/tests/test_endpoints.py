from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

# testar att health endpointen svarar med status ok
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# testar att uppladdning av giltig CSV ger 200 och rätt metadata
def test_upload_giltig_csv():
    csv_innehåll = b"Day,Close\n2024-01-01,42000\n2024-01-02,43000\n"
    response = client.post(
        "/data/upload",
        files={"file": ("test.csv", io.BytesIO(csv_innehåll), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json()["rows"] == 2
    assert "Close" in response.json()["columns"]

# testar att uppladdning av fel filtyp ger 400
def test_upload_ogiltig_filtyp():
    response = client.post(
        "/data/upload",
        files={"file": ("test.txt", io.BytesIO(b"inte en csv"), "text/plain")}
    )
    assert response.status_code == 400

# testar att /data/stats ger 404 om ingen fil är uppladdad
def test_stats_utan_uppladdning():
    import app.main as main_module
    main_module.uploaded_df = None
    response = client.get("/data/stats")
    assert response.status_code == 404