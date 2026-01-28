"""
Unit tests for Face Verification Providers.
"""
import unittest
from io import BytesIO
from PIL import Image
from attendance.providers.dummy_provider import DummyProvider


class DummyProviderTestCase(unittest.TestCase):
    """Tests para DummyProvider."""
    
    def setUp(self):
        """Configurar test."""
        self.provider = DummyProvider(demo_mode=True)
    
    def _create_test_image(self, size=(100, 100)) -> bytes:
        """Crear imagen de prueba."""
        img = Image.new('RGB', size, color='red')
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        return buffer.getvalue()
    
    def test_provider_name(self):
        """Test nombre del proveedor."""
        self.assertEqual(self.provider.name, 'dummy')
    
    def test_verify_same_image(self):
        """Test verificación con misma imagen."""
        image_bytes = self._create_test_image()
        result = self.provider.verify(image_bytes, image_bytes)
        
        self.assertIn('score', result)
        self.assertIn('match', result)
        self.assertIn('provider', result)
        self.assertEqual(result['provider'], 'dummy')
        self.assertEqual(result['score'], 1.0)
        self.assertTrue(result['match'])
    
    def test_verify_different_images(self):
        """Test verificación con imágenes diferentes."""
        ref_image = self._create_test_image(size=(100, 100))
        cap_image = self._create_test_image(size=(200, 200))
        
        result = self.provider.verify(ref_image, cap_image)
        
        self.assertIn('score', result)
        self.assertIn('match', result)
        self.assertGreaterEqual(result['score'], 0.0)
        self.assertLessEqual(result['score'], 1.0)
    
    def test_demo_mode_high_score(self):
        """Test modo demo con código especial."""
        image_bytes = self._create_test_image()
        
        # Código que termina en 001 debería dar score alto
        result = self.provider.verify(
            image_bytes,
            image_bytes,
            employee_code='EMP001'
        )
        
        self.assertEqual(result['score'], 0.95)
        self.assertTrue(result['match'])
    
    def test_demo_mode_demo_code(self):
        """Test modo demo con código DEMO."""
        image_bytes = self._create_test_image()
        
        result = self.provider.verify(
            image_bytes,
            image_bytes,
            employee_code='DEMO'
        )
        
        self.assertEqual(result['score'], 0.95)
        self.assertTrue(result['match'])
    
    def test_deterministic_score(self):
        """Test que el score sea determinístico."""
        ref_image = self._create_test_image(size=(100, 100))
        cap_image = self._create_test_image(size=(150, 150))
        
        result1 = self.provider.verify(ref_image, cap_image)
        result2 = self.provider.verify(ref_image, cap_image)
        
        # El score debe ser el mismo para las mismas imágenes
        self.assertEqual(result1['score'], result2['score'])


if __name__ == '__main__':
    unittest.main()
