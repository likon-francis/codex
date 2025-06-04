import React, { useEffect, useState } from 'react';

function CustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [newName, setNewName] = useState('');

  useEffect(() => {
    fetch('/customers')
      .then(res => res.json())
      .then(data => setCustomers(data))
      .catch(() => setCustomers([]));
  }, []);

  const addCustomer = e => {
    e.preventDefault();
    if (!newName.trim()) return;
    fetch('/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newName })
    })
      .then(res => res.json())
      .then(() => {
        setNewName('');
        return fetch('/customers');
      })
      .then(res => res.json())
      .then(data => setCustomers(data));
  };

  return (
    <div>
      <h2>Customers</h2>
      <form onSubmit={addCustomer}>
        <input
          value={newName}
          onChange={e => setNewName(e.target.value)}
          placeholder="New customer name"
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {customers.map(c => (
          <li key={c.id}>{c.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default CustomersPage;
