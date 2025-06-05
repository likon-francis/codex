from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
import secrets
from datetime import datetime
from sqlmodel import Field, Session, SQLModel, select

from database import init_db, get_session
import os

from iot_mqtt import MQTTClient
from analyzer import extract_text, analyze_text, list_presets

app = FastAPI(title="Codex Platform API")

# Initialize a placeholder MQTT client. In a real deployment this would
# connect to an MQTT broker (e.g., using paho-mqtt).
mqtt_client = MQTTClient()

# Initialize SQLite database
init_db()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

security = HTTPBasic()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class DoorAccessSyncRequest(SQLModel):
    controller_url: str

class IoTData(SQLModel):
    device_id: str
    payload: dict

class MQTTPublish(SQLModel):
    topic: str
    payload: str

class Visitor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str
    path: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    prompt: Optional[str] = None
    analysis_type: Optional[str] = None
    result: Optional[str] = None


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    """Simple HTTP Basic auth."""
    with get_session() as session:
        statement = select(User).where(User.username == credentials.username)
        user = session.exec(statement).first()
        if not user or not secrets.compare_digest(user.password, credentials.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

@app.get("/")
def read_root():
    return {"message": "Codex backend API"}


@app.post("/signup", response_model=User)
def signup(user: User):
    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.get("/me", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# --- Customer Module ---
door_access_sync_state = {}

@app.get("/customers", response_model=List[Customer])
def list_customers():
    """Return all customers from the database."""
    with get_session() as session:
        customers = session.exec(select(Customer)).all()
        return customers

@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer):
    with get_session() as session:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

# --- Door Access Control Module ---
@app.get("/door-access")
def list_door_access():
    """Placeholder for listing door access settings."""
    return door_access_sync_state

@app.post("/door-access/sync")
def sync_door_access(request: DoorAccessSyncRequest):
    """Stub endpoint to sync with local door access controller."""
    door_access_sync_state.update({"last_synced_with": request.controller_url})
    return door_access_sync_state

# --- IoT Module ---
@app.get("/iot")
def list_iot_devices():
    """Placeholder for listing registered IoT devices."""
    return []

@app.post("/iot/data")
def ingest_iot_data(data: IoTData):
    """Accept IoT data from external vendors."""
    return {"received": data.device_id}

@app.post("/iot/mqtt")
def publish_iot_message(msg: MQTTPublish):
    """Publish an MQTT message via the placeholder client."""
    mqtt_client.publish(msg.topic, msg.payload)
    return {"published": msg.topic}

@app.get("/iot/mqtt/messages")
def list_iot_messages():
    """Return MQTT messages received via the placeholder client."""
    return mqtt_client.messages
# --- Document Analyzer Module ---
@app.post("/analyze", response_model=Document)
async def analyze_document(
    file: UploadFile = File(...),
    prompt: str = Form(""),
    analysis_type: str = Form(""),
    current_user: User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in {".pdf", ".doc", ".docx", ".txt"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    data = await file.read()
    text = extract_text(data, file.filename)
    try:
        result = analyze_text(prompt, text, analysis_type or None)
    except Exception:
        raise HTTPException(status_code=502, detail="Analysis service failure")
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(data)
    doc = Document(
        filename=file.filename,
        path=path,
        prompt=prompt or None,
        analysis_type=analysis_type or None,
        result=result,
    )
    with get_session() as session:
        session.add(doc)
        session.commit()
        session.refresh(doc)
        return doc

@app.get("/documents", response_model=List[Document])
def list_documents(current_user: User = Depends(get_current_user)):
    with get_session() as session:
        docs = session.exec(select(Document)).all()
        return docs


@app.get("/documents/{doc_id}", response_model=Document)
def get_document(doc_id: int, current_user: User = Depends(get_current_user)):
    with get_session() as session:
        doc = session.get(Document, doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc


@app.get("/analysis-presets")
def get_analysis_presets():
    return list_presets()


# --- Visitor Registration Module ---

@app.get("/visitors", response_model=List[Visitor])
def list_visitors():
    """Return all visitors from the database."""
    with get_session() as session:
        visitors = session.exec(select(Visitor)).all()
        return visitors

@app.post("/visitors", response_model=Visitor)
def create_visitor(visitor: Visitor):
    with get_session() as session:
        session.add(visitor)
        session.commit()
        session.refresh(visitor)
        return visitor
