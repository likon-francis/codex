from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from iot_mqtt import MQTTClient

app = FastAPI(title="Codex Platform API")

# Initialize a placeholder MQTT client. In a real deployment this would
# connect to an MQTT broker (e.g., using paho-mqtt).
mqtt_client = MQTTClient()

class Customer(BaseModel):
    id: int
    name: str

class DoorAccessSyncRequest(BaseModel):
    controller_url: str

class IoTData(BaseModel):
    device_id: str
    payload: dict

class MQTTPublish(BaseModel):
    topic: str
    payload: str

class Visitor(BaseModel):
    id: int
    name: str

@app.get("/")
def read_root():
    return {"message": "Codex backend API"}

# --- Customer Module ---
fake_customers: List[Customer] = []
door_access_sync_state = {}

@app.get("/customers", response_model=List[Customer])
def list_customers():
    """Return all customers (in-memory placeholder)."""
    return fake_customers

@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer):
    fake_customers.append(customer)
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
fake_visitors: List[Visitor] = []

@app.get("/visitors", response_model=List[Visitor])
def list_visitors():
    """Return all visitors (in-memory placeholder)."""
    return fake_visitors

@app.post("/visitors", response_model=Visitor)
def create_visitor(visitor: Visitor):
    fake_visitors.append(visitor)
    return visitor
