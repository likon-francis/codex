# Backend

This is a minimal FastAPI backend exposing placeholder endpoints for each module:

- `/customers` – customer profile management (`GET`/`POST`)
- `/door-access` – door access control settings (`GET`)
- `/door-access/sync` – sync with local controller (`POST`)
- `/iot` – IoT device management (`GET`)
- `/iot/data` – ingest IoT signals (`POST`)
- `/iot/mqtt` – publish an MQTT message (`POST`)
- `/iot/mqtt/messages` – list received MQTT messages (`GET`)
- `/visitors` – visitor registration (`GET`/`POST`)
- `/analyze` - upload a document and return analysis (fields `file`, `prompt`,
  optional `analysis_type`). Pass `detect_type=true` to let the server guess the
  document type. `analysis_type` may be `cv` or `tender` to use default system
  prompts.

- `/documents` - list analyzed documents
- `/documents/{id}` - retrieve a single document
- `/analysis-presets` - list available preset analysis types
- `/signup` - create a user account
- `/me` - return the authenticated user

The analyzer extracts text from PDF, Word and plain‑text documents using
PyPDF2 and python-docx. Each stored record captures the filename,
detected or supplied analysis type, prompt, result and the time the file was
processed. When `detect_type=true` is supplied the server uses a few simple
heuristics to guess whether a file is a CV, tender or other document.

Authentication is handled with HTTP Basic credentials. Create an account via
`/signup` and include your username and password when calling analyzer
endpoints.

## Development

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlmodel requests PyPDF2 python-docx
   ```
3. Run the development server (this will create a local SQLite
   database `codex.db` on first run):
   ```bash
   uvicorn main:app --reload
   ```
