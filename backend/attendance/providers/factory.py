"""
Factory para crear instancias de Face Verification Providers.
"""
import logging
from django.conf import settings
from attendance.providers.dummy_provider import DummyProvider
from attendance.providers.face_verification_provider import FaceVerificationProvider

logger = logging.getLogger(__name__)


def get_face_verification_provider() -> FaceVerificationProvider:
    """
    Obtener instancia del proveedor de validación facial configurado.
    
    Returns:
        Instancia de FaceVerificationProvider
    """
    provider_name = getattr(settings, 'FACE_VERIFICATION_PROVIDER', 'dummy')
    
    if provider_name == 'dummy':
        return DummyProvider(demo_mode=True)
    else:
        raise ValueError(f"Proveedor desconocido: {provider_name}")
