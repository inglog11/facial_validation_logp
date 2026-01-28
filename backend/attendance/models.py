"""
Models for attendance system.
"""
from django.db import models
from django.core.validators import RegexValidator


class Employee(models.Model):
    """Modelo de empleado."""
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
    ]
    
    employee_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9_-]+$',
                message='El código de empleado solo puede contener letras mayúsculas, números, guiones y guiones bajos.'
            )
        ],
        verbose_name='Código de Empleado'
    )
    full_name = models.CharField(max_length=200, verbose_name='Nombre Completo')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Estado'
    )
    photo_ref = models.ImageField(
        upload_to='photos/',
        verbose_name='Foto de Referencia'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee_code']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee_code} - {self.full_name}"


class AttendanceEvent(models.Model):
    """Modelo de evento de asistencia (check-in)."""
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_events',
        verbose_name='Empleado'
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')
    score = models.FloatField(
        verbose_name='Score de Similitud',
        help_text='Score de similitud facial (0.0 - 1.0)'
    )
    decision = models.BooleanField(
        verbose_name='Decisión',
        help_text='True si el score >= threshold, False en caso contrario'
    )
    provider_name = models.CharField(
        max_length=100,
        verbose_name='Proveedor',
        help_text='Nombre del proveedor de validación facial usado'
    )
    threshold_used = models.FloatField(
        verbose_name='Umbral Aplicado',
        help_text='Umbral de validación usado en este check-in'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    
    class Meta:
        verbose_name = 'Evento de Asistencia'
        verbose_name_plural = 'Eventos de Asistencia'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['employee', '-timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['decision']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_code} - {self.timestamp} - {'✓' if self.decision else '✗'}"
