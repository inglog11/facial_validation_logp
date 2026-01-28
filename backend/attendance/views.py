"""
Views for attendance API.
"""
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.http import Http404
from attendance.models import Employee, AttendanceEvent
from attendance.serializers import (
    EmployeeSerializer,
    EmployeeCreateSerializer,
    EmployeeUpdateSerializer,
    CheckInSerializer,
    CheckInResponseSerializer,
    AttendanceEventSerializer,
)
from attendance.services import (
    CreateEmployeeService,
    UpdateEmployeeService,
    DeleteEmployeeService,
    CheckInEmployeeService,
)
from attendance.repositories import EmployeeRepository

logger = logging.getLogger(__name__)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de empleados.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    def get_serializer_class(self):
        """Retornar serializer apropiado según la acción."""
        if self.action == 'create':
            return EmployeeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EmployeeUpdateSerializer
        return EmployeeSerializer
    
    def create(self, request, *args, **kwargs):
        """Crear empleado."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            employee = serializer.save()
            response_serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creando empleado: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, *args, **kwargs):
        """Actualizar empleado."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        
        try:
            employee = serializer.save()
            response_serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(response_serializer.data)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error actualizando empleado: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def partial_update(self, request, *args, **kwargs):
        """Actualizar parcialmente empleado."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            employee = serializer.save()
            response_serializer = EmployeeSerializer(employee, context={'request': request})
            return Response(response_serializer.data)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error actualizando empleado: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, *args, **kwargs):
        """Eliminar empleado."""
        instance = self.get_object()
        
        try:
            service = DeleteEmployeeService()
            service.execute(instance.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Empleado no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error eliminando empleado: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Listar solo empleados activos."""
        active_employees = Employee.objects.filter(status='active')
        serializer = self.get_serializer(active_employees, many=True)
        return Response(serializer.data)


class CheckInView(APIView):
    """
    View para registrar entrada de empleados (check-in).
    """
    
    def post(self, request):
        """Registrar entrada mediante validación facial."""
        logger.info(f"Datos recibidos en check-in: {list(request.data.keys())}")
        logger.debug(f"Employee code recibido: {request.data.get('employee_code', 'NO ENCONTRADO')}")
        logger.debug(f"Imagen recibida (primeros 100 chars): {str(request.data.get('capture_image', 'NO ENCONTRADO'))[:100]}")
        
        serializer = CheckInSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Error de validación en check-in: {serializer.errors}")
            return Response(
                {'error': 'Error de validación', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        employee_code = serializer.validated_data['employee_code']
        capture_image = serializer.validated_data['capture_image']
        
        try:
            service = CheckInEmployeeService()
            result = service.execute(
                employee_code=employee_code,
                capture_image_data=capture_image
            )
            
            response_serializer = CheckInResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        except Employee.DoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error en check-in: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AttendanceEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para eventos de asistencia.
    """
    queryset = AttendanceEvent.objects.all()
    serializer_class = AttendanceEventSerializer
    
    def get_queryset(self):
        """Filtrar por employee_code si se proporciona."""
        queryset = AttendanceEvent.objects.all()
        employee_code = self.request.query_params.get('employee_code', None)
        
        if employee_code:
            queryset = queryset.filter(employee__employee_code=employee_code)
        
        return queryset.order_by('-timestamp')
