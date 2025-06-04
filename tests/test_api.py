from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_customer_crud():
    res = client.post("/customers", json={"name": "Alice"})
    assert res.status_code == 200
    cid = res.json()["id"]

    res = client.get(f"/customers/{cid}")
    assert res.status_code == 200

    res = client.put(f"/customers/{cid}", json={"name": "Alice Smith"})
    assert res.status_code == 200

    res = client.delete(f"/customers/{cid}")
    assert res.status_code == 200


def test_door_panel_crud():
    res = client.post(
        "/door-panels",
        json={"name": "Main Door", "location": "Front"},
    )
    assert res.status_code == 200
    pid = res.json()["id"]

    res = client.get(f"/door-panels/{pid}")
    assert res.status_code == 200

    res = client.delete(f"/door-panels/{pid}")
    assert res.status_code == 200


def test_door_group_crud():
    res = client.post("/door-groups", json={"name": "Admins"})
    assert res.status_code == 200
    gid = res.json()["id"]

    res = client.get(f"/door-groups/{gid}")
    assert res.status_code == 200

    res = client.delete(f"/door-groups/{gid}")
    assert res.status_code == 200


def test_iot_device_and_data():
    res = client.post("/iot/devices", json={"device_id": "sensor-1"})
    assert res.status_code == 200
    did = res.json()["id"]

    res = client.post(
        "/iot/data",
        json={"device_id": "sensor-1", "payload": {"temp": 22}},
    )
    assert res.status_code == 200

    res = client.get("/iot/data")
    assert res.status_code == 200
    assert any(ev["device_id"] == "sensor-1" for ev in res.json())

    res = client.delete(f"/iot/devices/{did}")
    assert res.status_code == 200


def test_visitor_crud():
    res = client.post("/visitors", json={"name": "Bob"})
    assert res.status_code == 200
    vid = res.json()["id"]

    res = client.get(f"/visitors/{vid}")
    assert res.status_code == 200

    res = client.delete(f"/visitors/{vid}")
    assert res.status_code == 200


def test_mqtt_publish_and_list():
    res = client.post(
        "/iot/mqtt",
        json={"topic": "test", "payload": "hello"},
    )
    assert res.status_code == 200

    res = client.get("/iot/mqtt/messages")
    assert res.status_code == 200
    assert any(m["topic"] == "test" for m in res.json())


def test_door_access_sync():
    res = client.post("/door-access/sync", json={"controller_url": "http://localhost"})
    assert res.status_code == 200
    assert res.json().get("last_synced_with") == "http://localhost"
