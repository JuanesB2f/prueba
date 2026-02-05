from openai import OpenAI
from typing import List, Dict
from config import OPENAI_MODEL, OPENAI_TIMEOUT

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = OPENAI_MODEL
        self.timeout = OPENAI_TIMEOUT

    def chat(self, messages: List[Dict]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                timeout=self.timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error en OpenAI: {str(e)}"

    def analyze_image(self, image_url: str, prompt: str = "Describe la imagen en detalle") -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }],
                timeout=self.timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error analizando imagen: {str(e)}"
