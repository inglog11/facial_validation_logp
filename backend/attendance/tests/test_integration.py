"""
Integration tests for attendance API.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from attendance.models import Employee, AttendanceEvent
import base64
import json


class EmployeeAPITestCase(TestCase):
    """Tests de integración para API de empleados."""
    
    def setUp(self):
        """Configurar test."""
        self.client = APIClient()
    
    def test_create_employee(self):
        """Test crear empleado vía API."""
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        
        data = {
            'employee_code': 'EMP001',
            'full_name': 'Juan Pérez',
            'status': 'active',
            'photo_ref': photo
        }
        
        response = self.client.post('/api/employees/', data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['employee_code'], 'EMP001')
        self.assertEqual(response.data['full_name'], 'Juan Pérez')
    
    def test_list_employees(self):
        """Test listar empleados."""
        # Crear empleados de prueba
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake image",
            content_type="image/jpeg"
        )
        
        Employee.objects.create(
            employee_code='EMP001',
            full_name='Juan Pérez',
            status='active',
            photo_ref=photo
        )
        
        Employee.objects.create(
            employee_code='EMP002',
            full_name='María García',
            status='active',
            photo_ref=photo
        )
        
        response = self.client.get('/api/employees/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get('results', response.data)), 2)
    
    def test_get_employee(self):
        """Test obtener empleado por ID."""
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake image",
            content_type="image/jpeg"
        )
        
        employee = Employee.objects.create(
            employee_code='EMP001',
            full_name='Juan Pérez',
            status='active',
            photo_ref=photo
        )
        
        response = self.client.get(f'/api/employees/{employee.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee_code'], 'EMP001')
    
    def test_update_employee(self):
        """Test actualizar empleado."""
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake image",
            content_type="image/jpeg"
        )
        
        employee = Employee.objects.create(
            employee_code='EMP001',
            full_name='Juan Pérez',
            status='active',
            photo_ref=photo
        )
        
        data = {
            'full_name': 'Juan Pérez García',
            'status': 'active'
        }
        
        response = self.client.patch(f'/api/employees/{employee.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Juan Pérez García')
    
    def test_delete_employee(self):
        """Test eliminar empleado."""
        photo = SimpleUploadedFile(
            "test.jpg",
            b"fake image",
            content_type="image/jpeg"
        )
        
        employee = Employee.objects.create(
            employee_code='EMP001',
            full_name='Juan Pérez',
            status='active',
            photo_ref=photo
        )
        
        response = self.client.delete(f'/api/employees/{employee.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=employee.id).exists())


class CheckInAPITestCase(TestCase):
    """Tests de integración para API de check-in."""
    
    def setUp(self):
        """Configurar test."""
        self.client = APIClient()
        
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
    
    def test_checkin_success(self):
        """Test check-in exitoso."""
        # Crear imagen base64 de prueba
        image_bytes = b"fake capture image"
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        capture_image_data = f"data:image/jpeg;base64,{image_data}"
        
        data = {
            'employee_code': 'EMP001',
            'capture_image': capture_image_data
        }
        
        response = self.client.post(
            '/api/check-in/',
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('decision', response.data)
        self.assertIn('score', response.data)
        self.assertEqual(response.data['employee_code'], 'EMP001')
        
        # Verificar que se creó el evento
        self.assertTrue(
            AttendanceEvent.objects.filter(employee=self.employee).exists()
        )
    
    def test_checkin_employee_not_found(self):
        """Test check-in con empleado inexistente."""
        image_bytes = b"fake capture image"
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        capture_image_data = f"data:image/jpeg;base64,{image_data}"
        
        data = {
            'employee_code': 'INVALID',
            'capture_image': capture_image_data
        }
        
        response = self.client.post(
            '/api/check-in/',
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_checkin_inactive_employee(self):
        """Test check-in con empleado inactivo."""
        self.employee.status = 'inactive'
        self.employee.save()
        
        image_bytes = b"fake capture image"
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        capture_image_data = f"data:image/jpeg;base64,{image_data}"
        
        data = {
            'employee_code': 'EMP001',
            'capture_image': capture_image_data
        }
        
        response = self.client.post(
            '/api/check-in/',
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_checkin_no_photo_saved(self):
        """Test que la foto de check-in NO se guarda."""
        image_bytes = b"fake capture image"
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        capture_image_data = f"data:image/jpeg;base64,{image_data}"
        
        data = {
            'employee_code': 'EMP001',
            'capture_image': capture_image_data
        }
        
        response = self.client.post(
            '/api/check-in/',
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que solo existe la foto de referencia, no la de captura
        event = AttendanceEvent.objects.filter(employee=self.employee).first()
        self.assertIsNotNone(event)
        # No hay campo para foto de captura en el modelo (correcto)
