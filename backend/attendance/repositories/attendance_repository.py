"""
Repository for AttendanceEvent model.
"""
from typing import List, Optional
from datetime import datetime
from attendance.models import AttendanceEvent, Employee


class AttendanceRepository:
    """Repositorio para acceso a datos de AttendanceEvent."""
    
    @staticmethod
    def create(
        employee: Employee,
        score: float,
        decision: bool,
        provider_name: str,
        threshold_used: float,
        timestamp: Optional[datetime] = None
    ) -> AttendanceEvent:
        """Crear nuevo evento de asistencia."""
        event = AttendanceEvent(
            employee=employee,
            score=score,
            decision=decision,
            provider_name=provider_name,
            threshold_used=threshold_used,
            timestamp=timestamp or datetime.now()
        )
        event.save()
        return event
    
    @staticmethod
    def get_by_employee(employee: Employee, limit: Optional[int] = None) -> List[AttendanceEvent]:
        """Obtener eventos de asistencia de un empleado."""
        queryset = AttendanceEvent.objects.filter(employee=employee).order_by('-timestamp')
        if limit:
            queryset = queryset[:limit]
        return list(queryset)
    
    @staticmethod
    def get_by_id(event_id: int) -> Optional[AttendanceEvent]:
        """Obtener evento por ID."""
        try:
            return AttendanceEvent.objects.get(id=event_id)
        except AttendanceEvent.DoesNotExist:
            return None
    
    @staticmethod
    def get_all(limit: Optional[int] = None) -> List[AttendanceEvent]:
        """Obtener todos los eventos."""
        queryset = AttendanceEvent.objects.all().order_by('-timestamp')
        if limit:
            queryset = queryset[:limit]
        return list(queryset)
