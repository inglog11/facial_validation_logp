import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { employeeAPI } from '../api';

function EmployeeForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = !!id;
  
  const [formData, setFormData] = useState({
    employee_code: '',
    full_name: '',
    status: 'active',
    photo_ref: null,
  });
  const [photoPreview, setPhotoPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEdit) {
      loadEmployee();
    }
  }, [id]);

  const loadEmployee = async () => {
    try {
      setLoading(true);
      const response = await employeeAPI.get(id);
      const employee = response.data;
      setFormData({
        employee_code: employee.employee_code,
        full_name: employee.full_name,
        status: employee.status,
        photo_ref: null,
      });
      setPhotoPreview(employee.photo_ref_url);
    } catch (err) {
      setError('Error al cargar empleado: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        photo_ref: file
      }));
      
      // Preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isEdit) {
        await employeeAPI.update(id, formData);
      } else {
        await employeeAPI.create(formData);
      }
      navigate('/');
    } catch (err) {
      setError('Error al guardar empleado: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  if (loading && isEdit) {
    return <div className="loading">Cargando...</div>;
  }

  return (
    <div className="card">
      <h2>{isEdit ? 'Editar Empleado' : 'Nuevo Empleado'}</h2>
      
      {error && <div className="error">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Código de Empleado *</label>
          <input
            type="text"
            name="employee_code"
            value={formData.employee_code}
            onChange={handleChange}
            required
            disabled={isEdit}
            placeholder="Ej: EMP001"
          />
        </div>

        <div className="form-group">
          <label>Nombre Completo *</label>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            required
            placeholder="Ej: Juan Pérez"
          />
        </div>

        <div className="form-group">
          <label>Estado *</label>
          <select
            name="status"
            value={formData.status}
            onChange={handleChange}
            required
          >
            <option value="active">Activo</option>
            <option value="inactive">Inactivo</option>
          </select>
        </div>

        <div className="form-group">
          <label>Foto de Referencia {!isEdit && '*'}</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            required={!isEdit}
          />
          {photoPreview && (
            <img 
              src={photoPreview} 
              alt="Preview"
              style={{ 
                marginTop: '10px', 
                maxWidth: '200px', 
                borderRadius: '4px',
                border: '1px solid #ddd'
              }}
            />
          )}
        </div>

        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? 'Guardando...' : (isEdit ? 'Actualizar' : 'Crear')}
        </button>
        
        <button 
          type="button" 
          className="btn btn-secondary"
          onClick={() => navigate('/')}
        >
          Cancelar
        </button>
      </form>
    </div>
  );
}

export default EmployeeForm;
