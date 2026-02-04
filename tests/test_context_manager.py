"""
Tests para Context Manager
"""
import unittest
from src.context_manager import ContextManager

class TestContextManager(unittest.TestCase):
    """Tests del manejador de contexto"""
    
    def setUp(self):
        """Preparación antes de cada test"""
        self.context = ContextManager(max_tokens=2000, reserved_tokens=500)
    
    def test_add_message_user(self):
        """Test: Agregar mensaje de usuario"""
        result = self.context.add_message("user", "Hola")
        self.assertTrue(result)
        self.assertEqual(len(self.context.messages), 1)
        self.assertEqual(self.context.messages[0]["role"], "user")
    
    def test_add_message_assistant(self):
        """Test: Agregar mensaje de asistente"""
        self.context.add_message("user", "Hola")
        result = self.context.add_message("assistant", "¡Hola! ¿Cómo estás?")
        self.assertTrue(result)
        self.assertEqual(len(self.context.messages), 2)
    
    def test_get_token_info(self):
        """Test: Obtener información de tokens"""
        self.context.add_message("user", "Hola")
        info = self.context.get_token_info()
        
        self.assertIn("used_tokens", info)
        self.assertIn("available_tokens", info)
        self.assertIn("percentage", info)
        self.assertIn("messages_count", info)
        self.assertEqual(info["messages_count"], 1)
    
    def test_clear_context(self):
        """Test: Limpiar contexto"""
        self.context.add_message("user", "Hola")
        self.context.add_message("assistant", "¡Hola!")
        self.assertEqual(len(self.context.messages), 2)
        
        self.context.clear()
        self.assertEqual(len(self.context.messages), 0)
    
    def test_get_messages_for_api(self):
        """Test: Obtener mensajes formateados para API"""
        self.context.add_message("user", "Hola")
        self.context.add_message("assistant", "¡Hola!")
        
        messages = self.context.get_messages_for_api()
        self.assertEqual(len(messages), 2)
        self.assertNotIn("timestamp", messages[0])

if __name__ == "__main__":
    unittest.main()
