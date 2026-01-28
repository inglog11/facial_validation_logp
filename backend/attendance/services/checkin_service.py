"""
Service for Check-in operations.
"""
import base64
import logging
from io import BytesIO
from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from attendance.repositories import EmployeeRepository, AttendanceRepository
from attendance.providers.factory import get_face_verification_provider
from attendance.models import Employee

logger = logging.getLogger(__name__)


class CheckInEmployeeService:
    """Servicio para registrar entrada de empleados."""
    
    def __init__(
        self,
        employee_repo: EmployeeRepository = None,
        attendance_repo: AttendanceRepository = None,
        provider=None
    ):
        self.employee_repo = employee_repo or EmployeeRepository()
        self.attendance_repo = attendance_repo or AttendanceRepository()
        self.provider = provider or get_face_verification_provider()
        self.threshold = getattr(settings, 'FACE_VERIFICATION_THRESHOLD', 0.80)
    
    def execute(
        self,
        employee_code: str,
        capture_image_data: str
    ) -> dict:
        """
        Registrar entrada de empleado mediante validación facial.
        
        Args:
            employee_code: Código del empleado
            capture_image_data: Imagen capturada en base64 (data:image/...;base64,...)
        
        Returns:
            Dict con:
                - decision: bool
                - score: float
                - threshold_used: float
                - employee_code: str
                - timestamp: str
        
        Raises:
            Employee.DoesNotExist: Si el empleado no existe
            ValidationError: Si la imagen es inválida o el empleado está inactivo
        """
        # Buscar empleado
        employee = self.employee_repo.get_by_code(employee_code)
        if not employee:
            raise Employee.DoesNotExist(f"Empleado con código {employee_code} no existe")
        
        # Validar que el empleado esté activo
        if employee.status != 'active':
            raise ValidationError(f"Empleado {employee_code} está inactivo")
        
        # Validar y procesar imagen capturada
        capture_image_bytes = self._process_capture_image(capture_image_data)
        
        # Leer imagen de referencia
        reference_image_bytes = self._read_reference_image(employee.photo_ref)
        
        # Verificar con el proveedor
        try:
            verification_result = self.provider.verify(
                reference_image_bytes=reference_image_bytes,
                capture_image_bytes=capture_image_bytes,
                employee_code=employee_code
            )
        except Exception as e:
            logger.error(f"Error en verificación facial para {employee_code}: {e}")
            raise ValidationError(f"Error en verificación facial: {str(e)}")
        
        score = verification_result['score']
        provider_match = verification_result.get('match', False)
        
        # Aplicar threshold configurado
        decision = score >= self.threshold
        
        # Guardar evento (sin guardar la foto de captura)
        from datetime import datetime
        event = self.attendance_repo.create(
            employee=employee,
            score=score,
            decision=decision,
            provider_name=verification_result['provider'],
            threshold_used=self.threshold,
            timestamp=datetime.now()
        )
        
        logger.info(
            f"Check-in registrado: {employee_code} - "
            f"score={score:.2f}, decision={decision}, threshold={self.threshold}"
        )
        
        return {
            'decision': decision,
            'score': score,
            'threshold_used': self.threshold,
            'employee_code': employee_code,
            'timestamp': event.timestamp.isoformat()
        }
    
    def _process_capture_image(self, image_data: str) -> bytes:
        """
        Procesar imagen capturada desde base64.
        
        Args:
            image_data: String base64 con prefijo data:image/...
        
        Returns:
            Bytes de la imagen procesada
        
        Raises:
            ValidationError: Si la imagen es inválida
        """
        try:
            # Extraer base64 del string data:image/...;base64,...
            if ',' in image_data:
                header, base64_data = image_data.split(',', 1)
            else:
                base64_data = image_data
            
            # Decodificar base64
            image_bytes = base64.b64decode(base64_data)
            
            # Validar que sea una imagen válida
            try:
                img = Image.open(BytesIO(image_bytes))
                img.verify()
            except Exception as e:
                raise ValidationError(f"Imagen inválida: {str(e)}")
            
            return image_bytes
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            logger.error(f"Error procesando imagen capturada: {e}")
            raise ValidationError(f"Error procesando imagen: {str(e)}")
    
    def _read_reference_image(self, photo_ref) -> bytes:
        """
        Leer imagen de referencia desde el archivo.
        
        Args:
            photo_ref: Campo ImageField del modelo
        
        Returns:
            Bytes de la imagen de referencia
        
        Raises:
            ValidationError: Si no se puede leer la imagen
        """
        try:
            photo_ref.open('rb')
            image_bytes = photo_ref.read()
            photo_ref.close()
            return image_bytes
        except Exception as e:
            logger.error(f"Error leyendo imagen de referencia: {e}")
            raise ValidationError(f"Error leyendo imagen de referencia: {str(e)}")
