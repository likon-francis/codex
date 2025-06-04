import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/customers">Customers</Link></li>
        <li><Link to="/door-access">Door Access</Link></li>
        <li><Link to="/iot">IoT Devices</Link></li>
        <li><Link to="/visitors">Visitors</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
