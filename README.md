# Codex Platform
- **Document Analyzer Module**: upload and analyze files via OpenRouter

The Document Analyzer accepts PDF, Word or text files. A small React portal in
`frontend/` lets you select the backend URL, upload a document with an optional
prompt and choose the analysis type from a dropdown list, then view the returned
analysis. The `analysis_type` may be `cv` or `tender` to apply built-in system
prompts (available via the new
`/analysis-presets` endpoint). Uploaded files are written to an `uploads/`
directory on the backend and results are stored in the same SQLite database that
holds customer and visitor records, including a timestamp for when each upload
was analyzed. Text extraction is handled using **PyPDF2**
and **python-docx**. The OpenRouter API key is read from the
`OPENROUTER_API_KEY` environment variable or the default in
`backend/analyzer.py`.

Authentication is handled with simple HTTP Basic credentials. Create a user via
`POST /signup` then include your username and password with requests to the
analyzer endpoints.

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
pip install fastapi uvicorn sqlmodel requests PyPDF2 python-docx
uvicorn main:app --reload
```

The backend persists customer and visitor data to a local SQLite database (`codex.db`). It also provides endpoints to ingest IoT data and sync door access settings.
The Document Analyzer module exposes `/analyze` for uploading files, `/documents` to list past analyses, `/documents/{id}` to retrieve a single result, and `/analysis-presets` to view built-in analysis types.

## Running the Frontend

The frontend is a minimal React app using Parcel for development. Install
dependencies with `npm install` and start the dev server:

```bash
cd frontend
npm install
npm run start
```

