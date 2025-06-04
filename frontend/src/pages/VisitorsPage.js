import React, { useEffect, useState } from 'react';

function VisitorsPage() {
  const [visitors, setVisitors] = useState([]);
  const [visitorName, setVisitorName] = useState('');

  useEffect(() => {
    fetch('/visitors')
      .then(res => res.json())
      .then(data => setVisitors(data))
      .catch(() => setVisitors([]));
  }, []);

  const addVisitor = e => {
    e.preventDefault();
    if (!visitorName.trim()) return;
    fetch('/visitors', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: visitorName })
    })
      .then(res => res.json())
      .then(() => {
        setVisitorName('');
        return fetch('/visitors');
      })
      .then(res => res.json())
      .then(data => setVisitors(data));
  };

  return (
    <div>
      <h2>Visitors</h2>
      <form onSubmit={addVisitor}>
        <input
          value={visitorName}
          onChange={e => setVisitorName(e.target.value)}
          placeholder="Visitor name"
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {visitors.map(v => (
          <li key={v.id}>{v.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default VisitorsPage;
