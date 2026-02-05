from config import OPENAI_API_KEY, CHATBOT_TIMEOUT
from context_manager import ContextManager
from openai_service import OpenAIService
from command_handler import CommandHandler
from chatbot import Chatbot

def main():
    context = ContextManager()
    openai_service = OpenAIService(api_key=OPENAI_API_KEY)
    commands = CommandHandler(context, openai_service)
    bot = Chatbot(context, openai_service, commands)
    bot.run()

if __name__ == "__main__":
    main()
