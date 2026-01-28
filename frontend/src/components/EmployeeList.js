import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { employeeAPI } from '../api';

function EmployeeList() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      setLoading(true);
      const response = await employeeAPI.list();
      setEmployees(response.data.results || response.data);
      setError(null);
    } catch (err) {
      setError('Error al cargar empleados: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, employeeCode) => {
    if (!window.confirm(`¿Está seguro de eliminar al empleado ${employeeCode}?`)) {
      return;
    }

    try {
      await employeeAPI.delete(id);
      loadEmployees();
    } catch (err) {
      alert('Error al eliminar empleado: ' + (err.response?.data?.error || err.message));
    }
  };

  if (loading) {
    return <div className="loading">Cargando...</div>;
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2>Lista de Empleados</h2>
        <Link to="/employees/new" className="btn btn-primary">
          Nuevo Empleado
        </Link>
      </div>
      
      {error && <div className="error">{error}</div>}

      {employees.length === 0 ? (
        <p style={{ marginTop: '20px' }}>No hay empleados registrados.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Estado</th>
              <th>Foto</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((employee) => (
              <tr key={employee.id}>
                <td>{employee.employee_code}</td>
                <td>{employee.full_name}</td>
                <td>
                  <span className={`status-badge status-${employee.status}`}>
                    {employee.status === 'active' ? 'Activo' : 'Inactivo'}
                  </span>
                </td>
                <td>
                  {employee.photo_ref_url && (
                    <img 
                      src={employee.photo_ref_url} 
                      alt={employee.full_name}
                      style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '4px' }}
                    />
                  )}
                </td>
                <td>
                  <Link 
                    to={`/employees/${employee.id}/edit`}
                    className="btn btn-secondary"
                    style={{ fontSize: '12px', padding: '5px 10px' }}
                  >
                    Editar
                  </Link>
                  <button
                    onClick={() => handleDelete(employee.id, employee.employee_code)}
                    className="btn btn-danger"
                    style={{ fontSize: '12px', padding: '5px 10px' }}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default EmployeeList;
