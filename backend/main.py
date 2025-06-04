from fastapi import FastAPI, HTTPException
from typing import List
from sqlmodel import Field, Session, SQLModel, select

from database import init_db, get_session

from iot_mqtt import MQTTClient

app = FastAPI(title="Codex Platform API")

# Initialize a placeholder MQTT client. In a real deployment this would
# connect to an MQTT broker (e.g., using paho-mqtt).
mqtt_client = MQTTClient()

# Initialize SQLite database
init_db()

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

@app.get("/")
def read_root():
    return {"message": "Codex backend API"}

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
