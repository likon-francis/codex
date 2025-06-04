# Backend

This is a minimal FastAPI backend exposing placeholder endpoints for each module:

- `/customers` – customer profile management (`GET`/`POST`, supports `?search=`)
- `/customers/{id}` – manage a single customer (`GET`/`PUT`/`DELETE`)
- `/door-access` – door access control settings (`GET`)
- `/door-access/sync` – sync with local controller (`POST`)
- `/door-panels` – door panel CRUD (`GET`/`POST`)
- `/door-panels/{id}` – manage a single door panel (`GET`/`PUT`/`DELETE`)
- `/door-groups` – door access group CRUD (`GET`/`POST`)
- `/door-groups/{id}` – manage a single door access group (`GET`/`PUT`/`DELETE`)
- `/iot/devices` – IoT device registry (`GET`/`POST`)
- `/iot/devices/{id}` – manage a single IoT device (`GET`/`PUT`/`DELETE`)
- `/iot/data` – ingest IoT signals (`POST`) and list events (`GET`)
- `/iot/mqtt` – publish an MQTT message (`POST`)
- `/iot/mqtt/messages` – list received MQTT messages (`GET`)
- `/visitors` – visitor registration (`GET`/`POST`)
- `/visitors/{id}` – manage a single visitor (`GET`/`PUT`/`DELETE`)

## Development

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlmodel supabase
   ```
3. (Optional) Set Supabase credentials if you want to use Supabase
   instead of the local SQLite database:
   ```bash
   export SUPABASE_URL=<your-url>
   export SUPABASE_KEY=<service-key>
   ```
4. Run the development server (this will create a local SQLite
   database `codex.db` on first run if Supabase is not configured):
   ```bash
   uvicorn main:app --reload
   ```

## Running Tests

Install dependencies and execute pytest from the repo root:

```bash
pip install -r ../requirements.txt
pytest -q
```

