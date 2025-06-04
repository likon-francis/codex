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
pip install fastapi uvicorn sqlmodel supabase
uvicorn main:app --reload
```

The backend persists customer, visitor, door panel and IoT device data to a
local SQLite database (`codex.db`) by default. You can connect to a Supabase
PostgreSQL instance by setting `SUPABASE_URL` and `SUPABASE_KEY` environment
variables. It also provides endpoints to ingest IoT data, publish MQTT messages,
and sync door access settings.

### HTTP API Highlights

- `GET /customers` / `POST /customers` – create or list customers (supports `?search=` query)
- `GET /customers/{id}` / `PUT` / `DELETE` – manage a single customer
- `GET /door-panels` / `POST /door-panels` – create or list door panels
- `GET /door-panels/{id}` / `PUT` / `DELETE` – manage a single door panel
- `GET /door-groups` / `POST /door-groups` – create or list door access groups
- `GET /door-groups/{id}` / `PUT` / `DELETE` – manage a single door access group
- `POST /door-access/sync` – sync door controller configuration
- `GET /iot/devices` / `POST /iot/devices` – register IoT devices
- `GET /iot/devices/{id}` / `PUT` / `DELETE` – manage a single IoT device
- `POST /iot/data` – submit IoT telemetry
- `GET /iot/data` – list collected IoT data
- `POST /iot/mqtt` – publish MQTT message (demo only)
- `GET /visitors` / `POST /visitors` – visitor registry
- `GET /visitors/{id}` / `PUT` / `DELETE` – manage a single visitor



## Running the Frontend

The React application lives in the `frontend/` directory. It now includes
simple forms so you can create customers, door panels, door groups, IoT
devices, and visitors directly from the browser. Install dependencies and start
the dev server:

```bash
cd frontend
npm install
npm run dev
```

It will connect to the backend running on `http://localhost:8000` by default. You
can change the fetch URLs in the source files if your backend runs elsewhere.

## Running Tests

Install dependencies and run pytest:

```bash
pip install -r requirements.txt
pytest -q
```

