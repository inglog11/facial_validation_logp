"""
Unit tests for Services.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from django.core.exceptions import ValidationError
from django.test import TestCase
from attendance.models import Employee
from attendance.services import (
    CreateEmployeeService,
    UpdateEmployeeService,
    DeleteEmployeeService,
    CheckInEmployeeService,
)
from attendance.repositories import EmployeeRepository, AttendanceRepository


class CreateEmployeeServiceTestCase(TestCase):
    """Tests para CreateEmployeeService."""
    
    def setUp(self):
        """Configurar test."""
        self.service = CreateEmployeeService()
    
    def test_create_employee_success(self):
        """Test creación exitosa de empleado."""
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        
        employee = self.service.execute(
            employee_code='EMP001',
            full_name='Juan Pérez',
            status='active',
            photo_ref=photo
        )
        
        self.assertIsNotNone(employee.id)
        self.assertEqual(employee.employee_code, 'EMP001')
        self.assertEqual(employee.full_name, 'Juan Pérez')
        self.assertEqual(employee.status, 'active')
    
    def test_create_employee_duplicate_code(self):
        """Test error al crear empleado con código duplicado."""
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        
        # Crear primer empleado
        self.service.execute(
            employee_code='EMP001',
            full_name='Juan Pérez',
            status='active',
            photo_ref=photo
        )
        
        # Intentar crear otro con mismo código
        with self.assertRaises(ValidationError):
            self.service.execute(
                employee_code='EMP001',
                full_name='Otro Nombre',
                status='active',
                photo_ref=photo
            )
    
    def test_create_employee_invalid_status(self):
        """Test error con status inválido."""
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        
        with self.assertRaises(ValidationError):
            self.service.execute(
                employee_code='EMP001',
                full_name='Juan Pérez',
                status='invalid',
                photo_ref=photo
            )


class CheckInEmployeeServiceTestCase(TestCase):
    """Tests para CheckInEmployeeService."""
    
    def setUp(self):
        """Configurar test."""
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Crear empleado de prueba
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake reference image",
            content_type="image/jpeg"
        )
        
        self.employee = Employee.objects.create(
            employee_code='EMP001',
            full_name='Juan Pérez',
            status='active',
            photo_ref=photo
        )
        
        # Mock del provider
        self.mock_provider = Mock()
        self.mock_provider.name = 'dummy'
        self.mock_provider.verify = Mock(return_value={
            'score': 0.85,
            'match': True,
            'provider': 'dummy'
        })
        
        self.service = CheckInEmployeeService(provider=self.mock_provider)
    
    def test_checkin_success(self):
        """Test check-in exitoso."""
        import base64
        
        # Crear imagen base64 de prueba
        image_data = base64.b64encode(b"fake capture image").decode('utf-8')
        capture_image_data = f"data:image/jpeg;base64,{image_data}"
        
        result = self.service.execute(
            employee_code='EMP001',
            capture_image_data=capture_image_data
        )
        
        self.assertTrue(result['decision'])
        self.assertEqual(result['score'], 0.85)
        self.assertEqual(result['employee_code'], 'EMP001')
        self.assertIn('timestamp', result)
    
    def test_checkin_employee_not_found(self):
        """Test error cuando empleado no existe."""
        import base64
        
        image_data = base64.b64encode(b"fake capture image").decode('utf-8')
        capture_image_data = f"data:image/jpeg;base64,{image_data}"
        
        with self.assertRaises(Employee.DoesNotExist):
            self.service.execute(
                employee_code='INVALID',
                capture_image_data=capture_image_data
            )
    
    def test_checkin_inactive_employee(self):
        """Test error cuando empleado está inactivo."""
        import base64
        
        # Marcar empleado como inactivo
        self.employee.status = 'inactive'
        self.employee.save()
        
        image_data = base64.b64encode(b"fake capture image").decode('utf-8')
        capture_image_data = f"data:image/jpeg;base64,{image_data}"
        
        with self.assertRaises(ValidationError):
            self.service.execute(
                employee_code='EMP001',
                capture_image_data=capture_image_data
            )
    
    def test_checkin_threshold_decision(self):
        """Test decisión basada en threshold."""
        import base64
        
        # Configurar threshold alto
        self.service.threshold = 0.90
        
        # Provider retorna score bajo
        self.mock_provider.verify.return_value = {
            'score': 0.75,
            'match': False,
            'provider': 'dummy'
        }
        
        image_data = base64.b64encode(b"fake capture image").decode('utf-8')
        capture_image_data = f"data:image/jpeg;base64,{image_data}"
        
        result = self.service.execute(
            employee_code='EMP001',
            capture_image_data=capture_image_data
        )
        
        # Score 0.75 < threshold 0.90, debe ser False
        self.assertFalse(result['decision'])
        self.assertEqual(result['score'], 0.75)


if __name__ == '__main__':
    unittest.main()
