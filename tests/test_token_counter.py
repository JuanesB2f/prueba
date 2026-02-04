"""
Tests para Token Counter
"""
import unittest
from src.token_counter import TokenCounter

class TestTokenCounter(unittest.TestCase):
    """Tests del contador de tokens"""
    
    def setUp(self):
        """Preparación antes de cada test"""
        self.counter = TokenCounter(model="gpt-4")
    
    def test_count_single_token(self):
        """Test: Contar tokens en texto simple"""
        text = "Hola"
        tokens = self.counter.count_tokens(text)
        self.assertGreater(tokens, 0)
        self.assertLess(tokens, 10)  # Debe ser pocos tokens
    
    def test_count_multiple_tokens(self):
        """Test: Contar tokens en texto largo"""
        text = "Esta es una conversación más larga que contiene varias palabras"
        tokens = self.counter.count_tokens(text)
        self.assertGreater(tokens, 5)  # Debe ser más de 5 tokens
    
    def test_count_messages_tokens(self):
        """Test: Contar tokens en mensajes"""
        messages = [
            {"role": "user", "content": "Hola"},
            {"role": "assistant", "content": "¡Hola! ¿Cómo estás?"}
        ]
        tokens = self.counter.count_messages_tokens(messages)
        self.assertGreater(tokens, 0)
        # Debe incluir overhead de mensajes
        self.assertGreater(tokens, self.counter.count_tokens("Hola¡Hola! ¿Cómo estás?"))

if __name__ == "__main__":
    unittest.main()
