class CommandHandler:
    def __init__(self, context_manager, openai_service):
        self.context = context_manager
        self.openai = openai_service

    def handle(self, user_input: str) -> bool:
        if user_input.startswith("/help"):
            print(self.help())
            return True

        if user_input.startswith("/clear"):
            self.context.clear()
            print("🧹 Contexto limpiado.")
            return True

        if user_input.startswith("/history"):
            print(f"Mensajes en contexto: {len(self.context.get_context())}")
            return True

        if user_input.startswith("/imagen"):
            parts = user_input.split(maxsplit=1)
            if len(parts) != 2:
                print("Uso: /imagen <url>")
                return True
            result = self.openai.analyze_image(parts[1])
            self.context.add_message("assistant", result)
            print(f"🖼️ Análisis: {result}")
            return True

        if user_input.startswith("/exit"):
            return False

        return None

    def help(self):
        return """
/help     Muestra comandos
/imagen   Analiza imagen desde URL
/clear    Limpia el contexto
/history  Muestra info del contexto
/exit     Salir
"""
