from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Codex Platform API")

class Customer(BaseModel):
    id: int
    name: str

class DoorAccessSyncRequest(BaseModel):
    controller_url: str

class IoTData(BaseModel):
    device_id: str
    payload: dict

class Visitor(BaseModel):
    id: int
    name: str

@app.get("/")
def read_root():
    return {"message": "Codex backend API"}

# --- Customer Module ---
fake_customers: List[Customer] = []

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
    return []

@app.post("/door-access/sync")
def sync_door_access(request: DoorAccessSyncRequest):
    """Stub endpoint to sync with local door access controller."""
    return {"synced_with": request.controller_url}

# --- IoT Module ---
@app.get("/iot")
def list_iot_devices():
    """Placeholder for listing registered IoT devices."""
    return []

@app.post("/iot/data")
def ingest_iot_data(data: IoTData):
    """Accept IoT data from external vendors."""
    return {"received": data.device_id}

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
