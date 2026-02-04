"""
Módulo para gestionar el contexto de la conversación
Implementa estrategia de sliding window con priorización
"""
from typing import List, Dict, Optional
from datetime import datetime
from src.token_counter import TokenCounter

class ContextManager:
    """
    Gestiona el historial de conversación y el consumo de tokens
    Estrategia: Mantener primeros N mensajes + últimos M mensajes
    """
    
    def __init__(self, max_tokens: int = 4000, reserved_tokens: int = 500, model: str = "gpt-4"):
        """
        Inicializa el manejador de contexto
        
        Args:
            max_tokens: Límite máximo de tokens (~4000 para GPT-4)
            reserved_tokens: Tokens reservados para respuesta del modelo
            model: Modelo OpenAI a usar
        """
        self.max_tokens = max_tokens
        self.reserved_tokens = reserved_tokens
        self.available_tokens = max_tokens - reserved_tokens
        self.messages: List[Dict[str, str]] = []
        self.token_counter = TokenCounter(model)
        self.system_prompt = (
            "Eres un asistente de IA útil, amable y honesto. "
            "Mantén el contexto de la conversación y responde de manera clara y concisa."
        )
    
    def add_message(self, role: str, content) -> bool:
        """
        Agrega un mensaje al historial
        
        Args:
            role: 'user', 'assistant', o 'system'
            content: Contenido del mensaje (string o lista para vision)
            
        Returns:
            True si se agregó, False si no pudo agregarse
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.messages.append(message)
        
        # Verificar si excedemos límite de tokens
        if self._get_total_tokens() > self.available_tokens:
            self.messages.pop()  # Revertir
            return self._apply_context_strategy(message)
        
        return True
    
    def _apply_context_strategy(self, new_message: Dict) -> bool:
        """
        Aplica estrategia de gestión de contexto cuando se excede límite
        Estrategia: Mantener primeros 2 mensajes (contexto inicial) + últimos 5
        
        Args:
            new_message: Nuevo mensaje a intentar agregar
            
        Returns:
            True si se logró hacer espacio
        """
        # Siempre mantener al menos primeros 2 mensajes (contexto inicial)
        MIN_INITIAL_MESSAGES = 2
        # Mantener últimos N mensajes antes del nuevo
        KEEP_RECENT_MESSAGES = 4
        
        if len(self.messages) <= MIN_INITIAL_MESSAGES + KEEP_RECENT_MESSAGES:
            return False  # No hay mucho que eliminar
        
        # Guardar primeros mensajes
        initial_messages = self.messages[:MIN_INITIAL_MESSAGES]
        # Guardar últimos mensajes
        recent_messages = self.messages[-(KEEP_RECENT_MESSAGES):]
        
        # Reconstruir con nueva estructura
        self.messages = initial_messages + recent_messages + [new_message]
        
        # Verificar nuevamente
        if self._get_total_tokens() > self.available_tokens:
            self.messages.pop()  # No se puede agregar
            return False
        
        return True
    
    def _get_total_tokens(self) -> int:
        """Calcula tokens totales del contexto actual"""
        # Contar sistema
        system_tokens = self.token_counter.count_tokens(self.system_prompt)
        # Contar mensajes
        messages_tokens = self.token_counter.count_messages_tokens(self.messages)
        
        return system_tokens + messages_tokens
    
    def get_messages_for_api(self) -> List[Dict]:
        """
        Obtiene los mensajes formateados para enviar a OpenAI API
        Elimina timestamps internos
        
        Returns:
            Lista de mensajes sin campos internos
        """
        formatted_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.messages
        ]
        return formatted_messages
    
    def get_token_info(self) -> Dict:
        """
        Retorna información sobre tokens usados
        
        Returns:
            Dict con información de tokens
        """
        total = self._get_total_tokens()
        return {
            "used_tokens": total,
            "available_tokens": self.available_tokens,
            "percentage": (total / self.available_tokens) * 100,
            "messages_count": len(self.messages)
        }
    
    def clear(self) -> None:
        """Limpia el historial de mensajes"""
        self.messages = []
    
    def get_history(self) -> List[Dict]:
        """
        Retorna el historial completo
        
        Returns:
            Lista de mensajes con timestamps
        """
        return self.messages.copy()
