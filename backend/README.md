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

## Development

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
3. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```
