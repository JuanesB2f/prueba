from typing import List, Dict
import tiktoken
from config import MAX_TOKENS, WINDOW_MESSAGES, OPENAI_MODEL

class ContextManager:
    def __init__(self):
        self.messages: List[Dict] = [
            {"role": "system", "content": "Eres un asistente útil y conversacional."}
        ]
        self.encoder = tiktoken.encoding_for_model(OPENAI_MODEL)

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._trim_context()

    def get_context(self) -> List[Dict]:
        return self.messages

    def clear(self):
        self.messages = self.messages[:1]

    def _count_tokens(self, messages):
        return sum(len(self.encoder.encode(m["content"])) for m in messages)

    def _trim_context(self):
        while self._count_tokens(self.messages) > MAX_TOKENS:
            # conserva system + últimos N
            self.messages = [self.messages[0]] + self.messages[-WINDOW_MESSAGES:]
