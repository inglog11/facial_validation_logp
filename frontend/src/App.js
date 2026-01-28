import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import EmployeeList from './components/EmployeeList';
import EmployeeForm from './components/EmployeeForm';
import CheckIn from './components/CheckIn';

function App() {
  return (
    <Router>
      <div className="container">
        <Header />
        <Routes>
          <Route path="/" element={<EmployeeList />} />
          <Route path="/employees/new" element={<EmployeeForm />} />
          <Route path="/employees/:id/edit" element={<EmployeeForm />} />
          <Route path="/check-in" element={<CheckIn />} />
        </Routes>
      </div>
    </Router>
  );
}

function Header() {
  const location = useLocation();
  
  return (
    <div className="header">
      <h1>Sistema de Registro de Entrada</h1>
      <p>Validación Facial</p>
      <nav className="nav">
        <Link 
          to="/" 
          className={location.pathname === '/' ? 'active' : ''}
        >
          Empleados
        </Link>
        <Link 
          to="/employees/new" 
          className={location.pathname === '/employees/new' ? 'active' : ''}
        >
          Nuevo Empleado
        </Link>
        <Link 
          to="/check-in" 
          className={location.pathname === '/check-in' ? 'active' : ''}
        >
          Check-in
        </Link>
      </nav>
    </div>
  );
}

export default App;
