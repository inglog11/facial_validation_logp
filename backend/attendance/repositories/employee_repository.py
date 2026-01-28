"""
Repository for Employee model.
"""
from typing import Optional, List
from django.core.exceptions import ValidationError
from attendance.models import Employee


class EmployeeRepository:
    """Repositorio para acceso a datos de Employee."""
    
    @staticmethod
    def get_by_id(employee_id: int) -> Optional[Employee]:
        """Obtener empleado por ID."""
        try:
            return Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_code(employee_code: str) -> Optional[Employee]:
        """Obtener empleado por código."""
        try:
            return Employee.objects.get(employee_code=employee_code)
        except Employee.DoesNotExist:
            return None
    
    @staticmethod
    def get_all(active_only: bool = False) -> List[Employee]:
        """Obtener todos los empleados."""
        queryset = Employee.objects.all()
        if active_only:
            queryset = queryset.filter(status='active')
        return list(queryset)
    
    @staticmethod
    def create(
        employee_code: str,
        full_name: str,
        status: str,
        photo_ref
    ) -> Employee:
        """Crear nuevo empleado."""
        employee = Employee(
            employee_code=employee_code,
            full_name=full_name,
            status=status,
            photo_ref=photo_ref
        )
        employee.full_clean()
        employee.save()
        return employee
    
    @staticmethod
    def update(
        employee: Employee,
        full_name: Optional[str] = None,
        status: Optional[str] = None,
        photo_ref=None
    ) -> Employee:
        """Actualizar empleado existente."""
        if full_name is not None:
            employee.full_name = full_name
        if status is not None:
            employee.status = status
        if photo_ref is not None:
            employee.photo_ref = photo_ref
        
        employee.full_clean()
        employee.save()
        return employee
    
    @staticmethod
    def delete(employee: Employee) -> None:
        """Eliminar empleado."""
        employee.delete()
    
    @staticmethod
    def exists_by_code(employee_code: str) -> bool:
        """Verificar si existe un empleado con el código dado."""
        return Employee.objects.filter(employee_code=employee_code).exists()
