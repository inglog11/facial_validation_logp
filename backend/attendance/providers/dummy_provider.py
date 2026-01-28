"""
Dummy Provider for Face Verification (simulación).
"""
import hashlib
import logging
from typing import Dict
from attendance.providers.face_verification_provider import FaceVerificationProvider

logger = logging.getLogger(__name__)


class DummyProvider(FaceVerificationProvider):
    """Proveedor simulado de validación facial para pruebas."""
    
    def __init__(self, demo_mode: bool = True):
        """
        Inicializar DummyProvider.
        
        Args:
            demo_mode: Si True, retorna score alto para códigos que cumplen condición demo
        """
        self.demo_mode = demo_mode
    
    @property
    def name(self) -> str:
        """Nombre del proveedor."""
        return 'dummy'
    
    def verify(
        self,
        reference_image_bytes: bytes,
        capture_image_bytes: bytes,
        employee_code: str = None
    ) -> Dict[str, any]:
        """
        Simular verificación facial.
        
        En modo demo, si employee_code termina en '001' o 'DEMO', retorna score alto.
        En modo normal, calcula score determinístico basado en hash de las imágenes.
        """
        # Modo demo: retornar score alto para ciertos códigos
        if self.demo_mode and employee_code:
            if employee_code.endswith('001') or employee_code.endswith('DEMO'):
                logger.info(f"DummyProvider: Modo demo activado para {employee_code}")
                return {
                    'score': 0.95,
                    'match': True,
                    'provider': self.name
                }
        
        # Score determinístico basado en hash de las imágenes
        # Esto permite que los tests sean reproducibles
        ref_hash = hashlib.md5(reference_image_bytes).hexdigest()
        cap_hash = hashlib.md5(capture_image_bytes).hexdigest()
        
        # Calcular score basado en similitud de hash y longitud
        # Si los hashes son iguales, score = 1.0
        # Si son diferentes, score basado en longitud y primeros caracteres
        if ref_hash == cap_hash:
            score = 1.0
        else:
            # Score basado en similitud de longitud y primeros caracteres
            length_similarity = min(len(reference_image_bytes), len(capture_image_bytes)) / \
                               max(len(reference_image_bytes), len(capture_image_bytes), 1)
            
            # Similitud de primeros caracteres del hash
            hash_similarity = sum(1 for i in range(min(8, len(ref_hash), len(cap_hash)))
                                 if ref_hash[i] == cap_hash[i]) / 8.0
            
            # Score combinado (promedio ponderado)
            score = (length_similarity * 0.3 + hash_similarity * 0.7)
            
            # Asegurar que el score esté en rango razonable para pruebas
            # Normalmente será bajo (0.2 - 0.5) para imágenes diferentes
            score = max(0.2, min(0.5, score))
        
        match = score >= 0.80  # Threshold por defecto
        
        logger.debug(
            f"DummyProvider: score={score:.2f}, match={match}, "
            f"ref_len={len(reference_image_bytes)}, cap_len={len(capture_image_bytes)}"
        )
        
        return {
            'score': round(score, 4),
            'match': match,
            'provider': self.name
        }
