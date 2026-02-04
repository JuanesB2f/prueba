"""
Módulo para manejar comandos del sistema
"""
from typing import Dict, Callable, Tuple, Optional
from src.context_manager import ContextManager
from src.openai_service import OpenAIService

class CommandHandler:
    """Manejador de comandos del chatbot"""
    
    def __init__(self, context: ContextManager, openai_service: OpenAIService):
        """
        Inicializa el manejador de comandos
        
        Args:
            context: Manejador de contexto
            openai_service: Servicio de OpenAI
        """
        self.context = context
        self.openai_service = openai_service
        
        # Mapeo de comandos a funciones
        self.commands: Dict[str, Callable] = {
            '/help': self.help_command,
            '/clear': self.clear_command,
            '/history': self.history_command,
            '/imagen': self.image_command,
            '/exit': self.exit_command,
        }
    
    def is_command(self, text: str) -> bool:
        """
        Verifica si el texto es un comando
        
        Args:
            text: Texto a verificar
            
        Returns:
            True si es un comando
        """
        return text.strip().startswith('/')
    
    def process_command(self, text: str) -> Tuple[str, bool]:
        """
        Procesa un comando
        
        Args:
            text: Texto del comando
            
        Returns:
            Tupla (respuesta, es_comando_válido)
        """
        parts = text.strip().split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command not in self.commands:
            return f"❌ Comando desconocido: {command}\nUsa /help para ver comandos disponibles", False
        
        return self.commands[command](args)
    
    def help_command(self, args: str = "") -> Tuple[str, bool]:
        """Muestra ayuda"""
        help_text = """
╔════════════════════════════════════════════════════╗
║           COMANDOS DISPONIBLES                     ║
╚════════════════════════════════════════════════════╝

/help              - Muestra esta lista de comandos
/imagen <URL>      - Analiza una imagen desde URL
/clear             - Limpia el contexto de la conversación
/history           - Muestra información de la conversación
/exit              - Termina el programa

EJEMPLOS:
  /imagen https://example.com/foto.jpg
  /history
  /clear

CONTEXTO:
  - Se mantiene automáticamente durante la conversación
  - Máximo ~4000 tokens de contexto
  - Escriba mensajes normales para chatear
"""
        return help_text, True
    
    def clear_command(self, args: str = "") -> Tuple[str, bool]:
        """Limpia el contexto"""
        self.context.clear()
        return "✅ Contexto de conversación limpiado", True
    
    def history_command(self, args: str = "") -> Tuple[str, bool]:
        """Muestra información del historial"""
        info = self.context.get_token_info()
        
        history_text = f"""
╔════════════════════════════════════════════════════╗
║           INFORMACIÓN DE CONVERSACIÓN              ║
╚════════════════════════════════════════════════════╝

📊 Estadísticas de Tokens:
  - Tokens usados: {info['used_tokens']}/{info['available_tokens']}
  - Porcentaje: {info['percentage']:.1f}%
  - Mensajes: {info['messages_count']}

📝 Últimos mensajes:
"""
        
        messages = self.context.get_history()
        if not messages:
            history_text += "  (No hay mensajes aún)\n"
        else:
            for msg in messages[-5:]:  # Últimos 5 mensajes
                role = "👤 Tú" if msg['role'] == 'user' else "🤖 Bot"
                content = msg['content'][:60] + "..." if len(str(msg['content'])) > 60 else msg['content']
                history_text += f"  {role}: {content}\n"
        
        history_text += "\n"
        return history_text, True
    
    def image_command(self, image_url: str) -> Tuple[str, bool]:
        """Analiza una imagen"""
        if not image_url.strip():
            return "❌ Por favor proporciona una URL: /imagen <URL>", False
        
        print("\n🖼️  Analizando imagen...")
        analysis, success = self.openai_service.analyze_image(image_url.strip())
        
        if success:
            # Agregar análisis al contexto
            self.context.add_message("assistant", f"[Análisis de imagen]\n{analysis}")
            return analysis, True
        else:
            return analysis, False
    
    def exit_command(self, args: str = "") -> Tuple[str, bool]:
        """Termina el programa"""
        return "👋 ¡Hasta luego!", True
