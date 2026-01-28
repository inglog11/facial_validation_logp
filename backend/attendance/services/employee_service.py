"""
Services for Employee operations.
"""
import logging
from typing import Optional
from django.core.exceptions import ValidationError
from attendance.repositories import EmployeeRepository
from attendance.models import Employee

logger = logging.getLogger(__name__)


class CreateEmployeeService:
    """Servicio para crear empleados."""
    
    def __init__(self, repository: EmployeeRepository = None):
        self.repository = repository or EmployeeRepository()
    
    def execute(
        self,
        employee_code: str,
        full_name: str,
        status: str,
        photo_ref
    ) -> Employee:
        """
        Crear nuevo empleado.
        
        Args:
            employee_code: Código único del empleado
            full_name: Nombre completo
            status: Estado (active/inactive)
            photo_ref: Archivo de imagen de referencia
        
        Returns:
            Employee creado
        
        Raises:
            ValidationError: Si el código ya existe o datos inválidos
        """
        # Validar que el código no exista
        if self.repository.exists_by_code(employee_code):
            raise ValidationError(f"Ya existe un empleado con el código {employee_code}")
        
        # Validar status
        if status not in ['active', 'inactive']:
            raise ValidationError(f"Status inválido: {status}. Debe ser 'active' o 'inactive'")
        
        try:
            employee = self.repository.create(
                employee_code=employee_code,
                full_name=full_name,
                status=status,
                photo_ref=photo_ref
            )
            logger.info(f"Empleado creado: {employee_code}")
            return employee
        except ValidationError as e:
            logger.error(f"Error al crear empleado {employee_code}: {e}")
            raise


class UpdateEmployeeService:
    """Servicio para actualizar empleados."""
    
    def __init__(self, repository: EmployeeRepository = None):
        self.repository = repository or EmployeeRepository()
    
    def execute(
        self,
        employee_id: int,
        full_name: Optional[str] = None,
        status: Optional[str] = None,
        photo_ref=None
    ) -> Employee:
        """
        Actualizar empleado existente.
        
        Args:
            employee_id: ID del empleado
            full_name: Nuevo nombre completo (opcional)
            status: Nuevo estado (opcional)
            photo_ref: Nueva foto de referencia (opcional)
        
        Returns:
            Employee actualizado
        
        Raises:
            Employee.DoesNotExist: Si el empleado no existe
            ValidationError: Si los datos son inválidos
        """
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise Employee.DoesNotExist(f"Empleado con ID {employee_id} no existe")
        
        # Validar status si se proporciona
        if status is not None and status not in ['active', 'inactive']:
            raise ValidationError(f"Status inválido: {status}. Debe ser 'active' o 'inactive'")
        
        try:
            updated_employee = self.repository.update(
                employee=employee,
                full_name=full_name,
                status=status,
                photo_ref=photo_ref
            )
            logger.info(f"Empleado actualizado: {employee.employee_code}")
            return updated_employee
        except ValidationError as e:
            logger.error(f"Error al actualizar empleado {employee.employee_code}: {e}")
            raise


class DeleteEmployeeService:
    """Servicio para eliminar empleados."""
    
    def __init__(self, repository: EmployeeRepository = None):
        self.repository = repository or EmployeeRepository()
    
    def execute(self, employee_id: int) -> None:
        """
        Eliminar empleado.
        
        Args:
            employee_id: ID del empleado
        
        Raises:
            Employee.DoesNotExist: Si el empleado no existe
        """
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise Employee.DoesNotExist(f"Empleado con ID {employee_id} no existe")
        
        employee_code = employee.employee_code
        self.repository.delete(employee)
        logger.info(f"Empleado eliminado: {employee_code}")
