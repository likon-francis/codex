import React, { useEffect, useState } from 'react';

function DoorAccessPage() {
  const [panels, setPanels] = useState([]);
  const [groups, setGroups] = useState([]);
  const [panelName, setPanelName] = useState('');
  const [panelLocation, setPanelLocation] = useState('');
  const [groupName, setGroupName] = useState('');

  useEffect(() => {
    fetch('/door-panels')
      .then(res => res.json())
      .then(data => setPanels(data))
      .catch(() => setPanels([]));
    fetch('/door-groups')
      .then(res => res.json())
      .then(data => setGroups(data))
      .catch(() => setGroups([]));
  }, []);

  const addPanel = e => {
    e.preventDefault();
    if (!panelName.trim()) return;
    fetch('/door-panels', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: panelName, location: panelLocation })
    })
      .then(res => res.json())
      .then(() => {
        setPanelName('');
        setPanelLocation('');
        return fetch('/door-panels');
      })
      .then(res => res.json())
      .then(data => setPanels(data));
  };

  const addGroup = e => {
    e.preventDefault();
    if (!groupName.trim()) return;
    fetch('/door-groups', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: groupName })
    })
      .then(res => res.json())
      .then(() => {
        setGroupName('');
        return fetch('/door-groups');
      })
      .then(res => res.json())
      .then(data => setGroups(data));
  };

  return (
    <div>
      <h2>Door Panels</h2>
      <form onSubmit={addPanel}>
        <input
          value={panelName}
          onChange={e => setPanelName(e.target.value)}
          placeholder="Name"
        />
        <input
          value={panelLocation}
          onChange={e => setPanelLocation(e.target.value)}
          placeholder="Location"
        />
        <button type="submit">Add Panel</button>
      </form>
      <ul>
        {panels.map(p => (
          <li key={p.id}>{p.name} ({p.location})</li>
        ))}
      </ul>
      <h2>Door Groups</h2>
      <form onSubmit={addGroup}>
        <input
          value={groupName}
          onChange={e => setGroupName(e.target.value)}
          placeholder="Group name"
        />
        <button type="submit">Add Group</button>
      </form>
      <ul>
        {groups.map(g => (
          <li key={g.id}>{g.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default DoorAccessPage;
