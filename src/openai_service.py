"""
Módulo para interactuar con OpenAI API
Maneja Chat Completions y Vision API
"""
import os
from typing import List, Dict, Optional, Tuple
from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
import requests
from requests.exceptions import RequestException

class OpenAIService:
    """Servicio para comunicarse con OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", timeout: int = 30):
        """
        Inicializa el servicio OpenAI
        
        Args:
            api_key: Clave API de OpenAI
            model: Modelo a usar
            timeout: Timeout en segundos
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.timeout = timeout
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> Tuple[str, bool]:
        """
        Solicita una respuesta de chat a OpenAI
        
        Args:
            messages: Lista de mensajes en formato OpenAI
            
        Returns:
            Tupla (respuesta, éxito)
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                timeout=self.timeout
            )
            return response.choices[0].message.content, True
        
        except RateLimitError as e:
            error_msg = (
                "⚠️  Límite de rate limit alcanzado. "
                "Espera un momento antes de intentar nuevamente."
            )
            return error_msg, False
        
        except APITimeoutError:
            error_msg = "⏱️  La solicitud ha expirado. Intenta nuevamente."
            return error_msg, False
        
        except APIConnectionError as e:
            error_msg = f"🌐 Error de conexión: {str(e)}"
            return error_msg, False
        
        except Exception as e:
            error_msg = f"❌ Error en OpenAI: {str(e)}"
            return error_msg, False
    
    def analyze_image(self, image_url: str) -> Tuple[str, bool]:
        """
        Analiza una imagen usando Vision API
        
        Args:
            image_url: URL de la imagen
            
        Returns:
            Tupla (análisis, éxito)
        """
        is_valid, error = self._validate_image_url(image_url)
        if not is_valid:
            return error, False
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analiza esta imagen en detalle. Describe qué ves."
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                max_tokens=1024,
                timeout=self.timeout
            )
            return response.choices[0].message.content, True
        
        except RateLimitError:
            return "⚠️  Límite de rate limit. Intenta después.", False
        except APITimeoutError:
            return "⏱️  Análisis de imagen expirado.", False
        except Exception as e:
            return f"❌ Error analizando imagen: {str(e)}", False
    
    def _validate_image_url(self, url: str) -> Tuple[bool, str]:
        """
        Valida que una URL de imagen sea accesible
        
        Args:
            url: URL a validar
            
        Returns:
            Tupla (es_válida, mensaje_error)
        """
        if not url.startswith(('http://', 'https://')):
            return False, "❌ La URL debe comenzar con http:// o https://"
        
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                if 'image' not in content_type:
                    return False, "❌ La URL no apunta a una imagen válida"
                return True, ""
            else:
                return False, f"❌ La URL retornó estado {response.status_code}"
        
        except RequestException as e:
            return False, f"❌ No se puede acceder a la URL: {str(e)}"
    
    def get_model_info(self) -> str:
        """Retorna información del modelo configurado"""
        return f"Modelo: {self.model} | Timeout: {self.timeout}s"
