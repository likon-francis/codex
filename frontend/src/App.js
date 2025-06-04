import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import CustomersPage from './pages/CustomersPage';
import DoorAccessPage from './pages/DoorAccessPage';
import IotPage from './pages/IotPage';
import VisitorsPage from './pages/VisitorsPage';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/customers" element={<CustomersPage />} />
        <Route path="/door-access" element={<DoorAccessPage />} />
        <Route path="/iot" element={<IotPage />} />
        <Route path="/visitors" element={<VisitorsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
