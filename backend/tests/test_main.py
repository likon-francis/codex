import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from main import app, SQLModel
from database import engine

SQLModel.metadata.create_all(engine)
client = TestClient(app)

def test_root():
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json()['message'] == 'Codex backend API'

