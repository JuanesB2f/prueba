"""
Módulo para contar tokens usando tiktoken
"""
import tiktoken
from typing import List, Dict

class TokenCounter:
    """Contador de tokens para OpenAI"""
    
    def __init__(self, model: str = "gpt-4"):
        """
        Inicializa el contador de tokens
        
        Args:
            model: Nombre del modelo OpenAI
        """
        self.model = model
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback a encoding más común
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """
        Cuenta los tokens en un texto
        
        Args:
            text: Texto a contar
            
        Returns:
            Número de tokens
        """
        return len(self.encoding.encode(text))
    
    def count_messages_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Cuenta los tokens de una lista de mensajes
        
        Args:
            messages: Lista de mensajes en formato OpenAI
            
        Returns:
            Número total de tokens
        """
        total_tokens = 0
        for message in messages:
            # Sumar tokens del contenido
            if isinstance(message["content"], str):
                total_tokens += self.count_tokens(message["content"])
            else:
                # Si es una lista (texto + imágenes)
                for content in message["content"]:
                    if content["type"] == "text":
                        total_tokens += self.count_tokens(content["text"])
                    elif content["type"] == "image_url":
                        # Las imágenes tienen costo fijo
                        total_tokens += 85  # Tokens base para imagen
            
            # Overhead de estructura del mensaje
            total_tokens += 4
        
        return total_tokens
