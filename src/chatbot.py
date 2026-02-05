class Chatbot:
    def __init__(self, context_manager, openai_service, command_handler):
        self.context = context_manager
        self.openai = openai_service
        self.commands = command_handler

    def run(self):
        print("🤖 Chatbot iniciado. /help para comandos.")
        while True:
            user_input = input("> ")

            command_result = self.commands.handle(user_input)
            if command_result is False:
                break
            if command_result is True:
                continue

            self.context.add_message("user", user_input)
            reply = self.openai.chat(self.context.get_context())
            self.context.add_message("assistant", reply)
            print(f"< Bot: {reply}")
