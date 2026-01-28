"""
Interface for Face Verification Providers.
"""
from abc import ABC, abstractmethod
from typing import Dict


class FaceVerificationProvider(ABC):
    """Interfaz abstracta para proveedores de validación facial."""
    
    @abstractmethod
    def verify(
        self,
        reference_image_bytes: bytes,
        capture_image_bytes: bytes,
        employee_code: str = None
    ) -> Dict[str, any]:
        """
        Verificar similitud entre imagen de referencia y captura.
        
        Args:
            reference_image_bytes: Bytes de la imagen de referencia
            capture_image_bytes: Bytes de la imagen capturada
            employee_code: Código del empleado (opcional, para modo demo)
        
        Returns:
            Dict con:
                - score: float (0.0 - 1.0)
                - match: bool
                - provider: str (nombre del proveedor)
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre del proveedor."""
        pass
