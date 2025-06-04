from fastapi import FastAPI, HTTPException
from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, select
from sqlalchemy import Column, JSON

from supabase_client import get_supabase_client

from database import init_db, get_session

from iot_mqtt import MQTTClient

app = FastAPI(title="Codex Platform API")

# Initialize a placeholder MQTT client. In a real deployment this would
# connect to an MQTT broker (e.g., using paho-mqtt).
mqtt_client = MQTTClient()

# Initialize Supabase client if environment variables are set. Operations
# fall back to local SQLite when no Supabase credentials are provided.
supabase = get_supabase_client()

class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class DoorPanel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    location: str | None = None

class DoorAccessGroup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None

class DoorAccessSyncRequest(SQLModel):
    controller_url: str

class IoTDevice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    device_id: str
    description: str | None = None

class IoTData(SQLModel):
    device_id: str
    payload: dict

class IoTEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    device_id: str
    payload: dict = Field(sa_column=Column(JSON))

class MQTTPublish(SQLModel):
    topic: str
    payload: str

class Visitor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

# Initialize SQLite database once all models are defined
init_db()

@app.get("/")
def read_root():
    return {"message": "Codex backend API"}

# --- Customer Module ---
door_access_sync_state = {}

@app.get("/customers", response_model=List[Customer])
def list_customers(search: Optional[str] = None):
    """Return all customers or filter by name using the ``search`` query parameter."""
    if supabase:
        query = supabase.table("customers").select("*")
        if search:
            query = query.ilike("name", f"%{search}%")
        res = query.execute()
        return res.data or []
    with get_session() as session:
        statement = select(Customer)
        if search:
            statement = statement.where(Customer.name.contains(search))
        return session.exec(statement).all()

@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer):
    if supabase:
        data = customer.dict(exclude_unset=True)
        res = supabase.table("customers").insert(data).execute()
        return Customer(**res.data[0])
    with get_session() as session:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    if supabase:
        res = (
            supabase.table("customers").select("*").eq("id", customer_id).execute()
        )
        if not res.data:
            raise HTTPException(status_code=404, detail="Customer not found")
        return Customer(**res.data[0])
    with get_session() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: Customer):
    data = customer.dict(exclude_unset=True)
    if supabase:
        res = (
            supabase.table("customers")
            .update(data)
            .eq("id", customer_id)
            .execute()
        )
        if not res.data:
            raise HTTPException(status_code=404, detail="Customer not found")
        return Customer(**res.data[0])
    with get_session() as session:
        db_customer = session.get(Customer, customer_id)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        for key, value in data.items():
            setattr(db_customer, key, value)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    if supabase:
        res = supabase.table("customers").delete().eq("id", customer_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {"deleted": customer_id}
    with get_session() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        session.delete(customer)
        session.commit()
        return {"deleted": customer_id}

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

@app.get("/door-panels", response_model=List[DoorPanel])
def list_door_panels():
    """List door access panels."""
    if supabase:
        res = supabase.table("door_panels").select("*").execute()
        return res.data or []
    with get_session() as session:
        return session.exec(select(DoorPanel)).all()

@app.post("/door-panels", response_model=DoorPanel)
def create_door_panel(panel: DoorPanel):
    """Create a new door panel."""
    if supabase:
        data = panel.dict(exclude_unset=True)
        res = supabase.table("door_panels").insert(data).execute()
        return DoorPanel(**res.data[0])
    with get_session() as session:
        session.add(panel)
        session.commit()
        session.refresh(panel)
        return panel

@app.get("/door-panels/{panel_id}", response_model=DoorPanel)
def get_door_panel(panel_id: int):
    if supabase:
        res = supabase.table("door_panels").select("*").eq("id", panel_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Door panel not found")
        return DoorPanel(**res.data[0])
    with get_session() as session:
        panel = session.get(DoorPanel, panel_id)
        if not panel:
            raise HTTPException(status_code=404, detail="Door panel not found")
        return panel

@app.put("/door-panels/{panel_id}", response_model=DoorPanel)
def update_door_panel(panel_id: int, panel: DoorPanel):
    data = panel.dict(exclude_unset=True)
    if supabase:
        res = (
            supabase.table("door_panels").update(data).eq("id", panel_id).execute()
        )
        if not res.data:
            raise HTTPException(status_code=404, detail="Door panel not found")
        return DoorPanel(**res.data[0])
    with get_session() as session:
        db_panel = session.get(DoorPanel, panel_id)
        if not db_panel:
            raise HTTPException(status_code=404, detail="Door panel not found")
        for key, value in data.items():
            setattr(db_panel, key, value)
        session.add(db_panel)
        session.commit()
        session.refresh(db_panel)
        return db_panel

@app.delete("/door-panels/{panel_id}")
def delete_door_panel(panel_id: int):
    if supabase:
        res = supabase.table("door_panels").delete().eq("id", panel_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Door panel not found")
        return {"deleted": panel_id}
    with get_session() as session:
        panel = session.get(DoorPanel, panel_id)
        if not panel:
            raise HTTPException(status_code=404, detail="Door panel not found")
        session.delete(panel)
        session.commit()
        return {"deleted": panel_id}

# --- Door Access Groups ---
@app.get("/door-groups", response_model=List[DoorAccessGroup])
def list_door_groups():
    """List door access groups."""
    if supabase:
        res = supabase.table("door_groups").select("*").execute()
        return res.data or []
    with get_session() as session:
        return session.exec(select(DoorAccessGroup)).all()


@app.post("/door-groups", response_model=DoorAccessGroup)
def create_door_group(group: DoorAccessGroup):
    """Create a new door access group."""
    if supabase:
        data = group.dict(exclude_unset=True)
        res = supabase.table("door_groups").insert(data).execute()
        return DoorAccessGroup(**res.data[0])
    with get_session() as session:
        session.add(group)
        session.commit()
        session.refresh(group)
        return group


@app.get("/door-groups/{group_id}", response_model=DoorAccessGroup)
def get_door_group(group_id: int):
    if supabase:
        res = supabase.table("door_groups").select("*").eq("id", group_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Door group not found")
        return DoorAccessGroup(**res.data[0])
    with get_session() as session:
        group = session.get(DoorAccessGroup, group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Door group not found")
        return group


@app.put("/door-groups/{group_id}", response_model=DoorAccessGroup)
def update_door_group(group_id: int, group: DoorAccessGroup):
    data = group.dict(exclude_unset=True)
    if supabase:
        res = (
            supabase.table("door_groups").update(data).eq("id", group_id).execute()
        )
        if not res.data:
            raise HTTPException(status_code=404, detail="Door group not found")
        return DoorAccessGroup(**res.data[0])
    with get_session() as session:
        db_group = session.get(DoorAccessGroup, group_id)
        if not db_group:
            raise HTTPException(status_code=404, detail="Door group not found")
        for key, value in data.items():
            setattr(db_group, key, value)
        session.add(db_group)
        session.commit()
        session.refresh(db_group)
        return db_group


@app.delete("/door-groups/{group_id}")
def delete_door_group(group_id: int):
    if supabase:
        res = supabase.table("door_groups").delete().eq("id", group_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Door group not found")
        return {"deleted": group_id}
    with get_session() as session:
        group = session.get(DoorAccessGroup, group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Door group not found")
        session.delete(group)
        session.commit()
        return {"deleted": group_id}

# --- IoT Module ---
@app.get("/iot/devices", response_model=List[IoTDevice])
def list_iot_devices():
    """Return all registered IoT devices."""
    if supabase:
        res = supabase.table("iot_devices").select("*").execute()
        return res.data or []
    with get_session() as session:
        return session.exec(select(IoTDevice)).all()

@app.post("/iot/devices", response_model=IoTDevice)
def register_iot_device(device: IoTDevice):
    """Register a new IoT device."""
    if supabase:
        data = device.dict(exclude_unset=True)
        res = supabase.table("iot_devices").insert(data).execute()
        return IoTDevice(**res.data[0])
    with get_session() as session:
        session.add(device)
        session.commit()
        session.refresh(device)
        return device

@app.get("/iot/devices/{device_id}", response_model=IoTDevice)
def get_iot_device(device_id: int):
    if supabase:
        res = supabase.table("iot_devices").select("*").eq("id", device_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Device not found")
        return IoTDevice(**res.data[0])
    with get_session() as session:
        device = session.get(IoTDevice, device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return device

@app.put("/iot/devices/{device_id}", response_model=IoTDevice)
def update_iot_device(device_id: int, device: IoTDevice):
    data = device.dict(exclude_unset=True)
    if supabase:
        res = (
            supabase.table("iot_devices").update(data).eq("id", device_id).execute()
        )
        if not res.data:
            raise HTTPException(status_code=404, detail="Device not found")
        return IoTDevice(**res.data[0])
    with get_session() as session:
        db_dev = session.get(IoTDevice, device_id)
        if not db_dev:
            raise HTTPException(status_code=404, detail="Device not found")
        for key, value in data.items():
            setattr(db_dev, key, value)
        session.add(db_dev)
        session.commit()
        session.refresh(db_dev)
        return db_dev

@app.delete("/iot/devices/{device_id}")
def delete_iot_device(device_id: int):
    if supabase:
        res = supabase.table("iot_devices").delete().eq("id", device_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Device not found")
        return {"deleted": device_id}
    with get_session() as session:
        device = session.get(IoTDevice, device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        session.delete(device)
        session.commit()
        return {"deleted": device_id}

@app.post("/iot/data")
def ingest_iot_data(data: IoTData):
    """Accept IoT data from external vendors."""
    if supabase:
        supabase.table("iot_data").insert(data.dict()).execute()
        return {"received": data.device_id}
    with get_session() as session:
        event = IoTEvent(device_id=data.device_id, payload=data.payload)
        session.add(event)
        session.commit()
        session.refresh(event)
        return {"received": event.id}

@app.get("/iot/data", response_model=List[IoTEvent])
def list_iot_data():
    """List stored IoT data events."""
    if supabase:
        res = supabase.table("iot_data").select("*").execute()
        return res.data or []
    with get_session() as session:
        return session.exec(select(IoTEvent)).all()

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
    if supabase:
        res = supabase.table("visitors").select("*").execute()
        return res.data or []
    with get_session() as session:
        visitors = session.exec(select(Visitor)).all()
        return visitors

@app.post("/visitors", response_model=Visitor)
def create_visitor(visitor: Visitor):
    if supabase:
        data = visitor.dict(exclude_unset=True)
        res = supabase.table("visitors").insert(data).execute()
        return Visitor(**res.data[0])
    with get_session() as session:
        session.add(visitor)
        session.commit()
        session.refresh(visitor)
        return visitor

@app.get("/visitors/{visitor_id}", response_model=Visitor)
def get_visitor(visitor_id: int):
    if supabase:
        res = supabase.table("visitors").select("*").eq("id", visitor_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Visitor not found")
        return Visitor(**res.data[0])
    with get_session() as session:
        visitor = session.get(Visitor, visitor_id)
        if not visitor:
            raise HTTPException(status_code=404, detail="Visitor not found")
        return visitor

@app.put("/visitors/{visitor_id}", response_model=Visitor)
def update_visitor(visitor_id: int, visitor: Visitor):
    data = visitor.dict(exclude_unset=True)
    if supabase:
        res = (
            supabase.table("visitors").update(data).eq("id", visitor_id).execute()
        )
        if not res.data:
            raise HTTPException(status_code=404, detail="Visitor not found")
        return Visitor(**res.data[0])
    with get_session() as session:
        db_visitor = session.get(Visitor, visitor_id)
        if not db_visitor:
            raise HTTPException(status_code=404, detail="Visitor not found")
        for key, value in data.items():
            setattr(db_visitor, key, value)
        session.add(db_visitor)
        session.commit()
        session.refresh(db_visitor)
        return db_visitor

@app.delete("/visitors/{visitor_id}")
def delete_visitor(visitor_id: int):
    if supabase:
        res = supabase.table("visitors").delete().eq("id", visitor_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Visitor not found")
        return {"deleted": visitor_id}
    with get_session() as session:
        visitor = session.get(Visitor, visitor_id)
        if not visitor:
            raise HTTPException(status_code=404, detail="Visitor not found")
        session.delete(visitor)
        session.commit()
        return {"deleted": visitor_id}
