
import os
from typing import Optional
from dotenv import load_dotenv
from src.context_manager import ContextManager
from src.openai_service import OpenAIService
from src.command_handler import CommandHandler

class Chatbot:
    """Chatbot conversacional con soporte de contexto e imágenes"""
    
    def __init__(self, api_key: Optional[str] = None):
        #  variables de entorno
        load_dotenv()
        
        # Configuración
        max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
        reserved_tokens = int(os.getenv("RESERVED_TOKENS_FOR_RESPONSE", "500"))
        model = os.getenv("OPENAI_MODEL", "gpt-4")
        timeout = int(os.getenv("OPENAI_TIMEOUT", "30"))
        
        # Inicializar componentes
        self.context = ContextManager(
            max_tokens=max_tokens,
            reserved_tokens=reserved_tokens,
            model=model
        )
        
        self.openai_service = OpenAIService(
            api_key=api_key,
            model=model,
            timeout=timeout
        )
        
        self.command_handler = CommandHandler(self.context, self.openai_service)
        self.running = False
    
    def send_message(self, user_input: str) -> Optional[str]:
        """
        Procesa un mensaje del usuario
        
        Args:
            user_input: Entrada del usuario
            
        Returns:
            Respuesta del bot o None si es /exit
        """
        # Verificar si es comando
        if self.command_handler.is_command(user_input):
            response, _ = self.command_handler.process_command(user_input)
            return response
        
        # Agregar mensaje del usuario al contexto
        added = self.context.add_message("user", user_input)
        if not added:
            return "⚠️  No se pudo agregar el mensaje. El contexto está lleno."
        
        # Obtener mensajes para API
        system_message = {"role": "system", "content": self.context.system_prompt}
        messages = [system_message] + self.context.get_messages_for_api()
        
        # Solicitar respuesta a OpenAI
        response, success = self.openai_service.chat_completion(messages)
        
        if success:
            # Agregar respuesta al contexto
            self.context.add_message("assistant", response)
            return response
        else:
            return response
    
    def get_info(self) -> str:
        """Retorna información del chatbot"""
        info = self.context.get_token_info()
        model_info = self.openai_service.get_model_info()
        
        return f"{model_info} | Tokens: {info['used_tokens']}/{info['available_tokens']}"
    
    def reset(self) -> None:
        """Reinicia el chatbot"""
        self.context.clear()
