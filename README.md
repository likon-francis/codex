# Codex Platform

This repository contains a simple skeleton for a multi-module platform. Modules include:

- **Customer Module**: customer profile management
- **Door Access Control Module**: manage door hardware and settings
- **IoT Module**: receive IoT signals via API or MQTT
- **Visitor Registration Module**
- **Document Analyzer Module**: upload and analyze files via OpenRouter

The IoT module now exposes simple MQTT helper endpoints so that external
vendors can push messages to the system. Door access synchronization state is
tracked in-memory for demonstration purposes.

## Structure

- `backend/` – FastAPI backend exposing module endpoints
- `frontend/` – React app with a simple document upload portal

Each module can be expanded as development continues.

## Running the Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlmodel requests
uvicorn main:app --reload
```

The backend persists customer and visitor data to a local SQLite database (`codex.db`). It also provides endpoints to ingest IoT data and sync door access settings.
The Document Analyzer module exposes `/analyze` for uploading files and `/documents` to list past analyses.

## Running the Frontend

The frontend is a minimal React app. Install dependencies with `npm install` and
start your preferred development server:

```bash
cd frontend
npm install
npm run start
```
