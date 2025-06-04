# Codex Platform

This repository contains a simple skeleton for a multi-module platform. Modules include:

- **Customer Module**: customer profile management
- **Door Access Control Module**: manage door hardware and settings
- **IoT Module**: receive IoT signals via API or MQTT
- **Visitor Registration Module**

The IoT module now exposes simple MQTT helper endpoints so that external
vendors can push messages to the system. Door access synchronization state is
tracked in-memory for demonstration purposes.

## Structure

- `backend/` – FastAPI backend exposing module endpoints
- `frontend/` – React placeholder app

Each module can be expanded as development continues.

## Running the Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic
uvicorn main:app --reload
```

The backend now includes in-memory endpoints to create and list customers and visitors, ingest IoT data, and sync door access settings.
