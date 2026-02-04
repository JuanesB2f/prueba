"""
Punto de entrada del chatbot CLI
Interfaz de línea de comandos interactiva
"""
import sys
import os
from src.chatbot import Chatbot

def print_welcome():
    """Imprime mensaje de bienvenida"""
    print("""
╔════════════════════════════════════════════════════╗
║         🤖 CHATBOT CONVERSACIONAL                  ║
║         Senior Backend Engineer Challenge          ║
╚════════════════════════════════════════════════════╝

Escribe /help para ver los comandos disponibles
Escribe /exit para terminar
""")

def print_prompt():
    """Imprime el prompt del usuario"""
    sys.stdout.write("\n> ")
    sys.stdout.flush()

def main():
    """Función principal"""
    try:
        # Inicializar chatbot
        chatbot = Chatbot()
        print_welcome()
        print(f"✅ {chatbot.get_info()}\n")
        
        # Loop principal
        while True:
            print_prompt()
            
            try:
                user_input = input().strip()
            except EOFError:
                print("\n")
                break
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            
            if not user_input:
                continue
            
            # Procesar entrada
            if user_input.lower() == '/exit':
                print("👋 ¡Hasta luego!")
                break
            
            response = chatbot.send_message(user_input)
            if response:
                print(f"\n🤖 {response}")
    
    except ValueError as e:
        print(f"❌ Error de configuración: {str(e)}")
        print("\nAsegúrate de configurar OPENAI_API_KEY en .env")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
