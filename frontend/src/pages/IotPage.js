import React, { useEffect, useState } from 'react';

function IotPage() {
  const [devices, setDevices] = useState([]);
  const [events, setEvents] = useState([]);
  const [deviceId, setDeviceId] = useState('');
  const [payload, setPayload] = useState('');

  useEffect(() => {
    fetch('/iot/devices')
      .then(res => res.json())
      .then(data => setDevices(data))
      .catch(() => setDevices([]));
    fetch('/iot/data')
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(() => setEvents([]));
  }, []);

  const addDevice = e => {
    e.preventDefault();
    if (!deviceId.trim()) return;
    fetch('/iot/devices', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ device_id: deviceId })
    })
      .then(res => res.json())
      .then(() => {
        setDeviceId('');
        return fetch('/iot/devices');
      })
      .then(res => res.json())
      .then(data => setDevices(data));
  };

  const sendData = e => {
    e.preventDefault();
    if (!deviceId.trim() || !payload.trim()) return;
    let dataObj;
    try {
      dataObj = JSON.parse(payload);
    } catch {
      alert('Payload must be valid JSON');
      return;
    }
    fetch('/iot/data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ device_id: deviceId, payload: dataObj })
    })
      .then(res => res.json())
      .then(() => {
        setPayload('');
        return fetch('/iot/data');
      })
      .then(res => res.json())
      .then(data => setEvents(data));
  };

  return (
    <div>
      <h2>IoT Devices</h2>
      <form onSubmit={addDevice}>
        <input
          value={deviceId}
          onChange={e => setDeviceId(e.target.value)}
          placeholder="Device ID"
        />
        <button type="submit">Register</button>
      </form>
      <ul>
        {devices.map(d => (
          <li key={d.id}>{d.device_id}</li>
        ))}
      </ul>
      <h3>Recent Data</h3>
      <form onSubmit={sendData}>
        <input
          value={payload}
          onChange={e => setPayload(e.target.value)}
          placeholder='{"temp": 22}'
        />
        <button type="submit">Send</button>
      </form>
      <ul>
        {events.map(e => (
          <li key={e.id}>{e.device_id}: {JSON.stringify(e.payload)}</li>
        ))}
      </ul>
    </div>
  );
}

export default IotPage;
