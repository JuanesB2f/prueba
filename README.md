# 🤖 Chatbot Conversacional - Prueba Técnica Senior Backend

Chatbot CLI conversacional que interactúa con OpenAI API, mantiene contexto, y analiza imágenes.

## 📋 Requisitos

- Python 3.8+
- OpenAI API Key

## 🚀 Instalación

### 1. Configurar Entorno

```bash
# Clonar o navegar al proyecto
cd /Users/macbook/Desktop/prueba

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar API Key

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu OpenAI API Key
nano .env
# O usa tu editor favorito
```

**Archivo .env:**
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_TIMEOUT=30
MAX_TOKENS=4000
RESERVED_TOKENS_FOR_RESPONSE=500
```

## 🎯 Estructura del Proyecto

```
/src
├── main.py                    # CLI entry point
├── chatbot.py                 # Orquestador principal
├── context_manager.py         # Gestión de contexto y tokens
├── openai_service.py          # Llamadas a OpenAI API
├── command_handler.py         # Procesamiento de comandos
└── token_counter.py           # Conteo de tokens

/tests
├── test_context_manager.py    # Tests de contexto
├── test_token_counter.py      # Tests de tokens
└── __init__.py

.env.example                   # Plantilla de variables
requirements.txt               # Dependencias Python
README.md                      # Este archivo
```

## 📖 Uso

### Iniciar el Chatbot

```bash
python3 -m src.main
```

### Ejemplos de Interacción

```
> Hola, mi nombre es Carlos
🤖 ¡Hola Carlos! Encantado de conocerte. ¿En qué puedo ayudarte hoy?

> Necesito ideas para un proyecto de machine learning
🤖 Claro Carlos, aquí algunas ideas interesantes...
   1. Sistema de predicción de precios inmobiliarios
   2. Clasificador de sentimientos en redes sociales
   ... [más ideas]

> ¿Cuál es mi nombre?
🤖 Tu nombre es Carlos

> /imagen https://example.com/foto.jpg
🤖 [Analizando imagen...]
🤖 En la imagen veo una persona con cabello castaño, usando lentes...

> ¿De qué color es el cabello?
🤖 Según la imagen que compartiste, el cabello es castaño
```

## 🎮 Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `/help` | Muestra lista de comandos |
| `/imagen <URL>` | Analiza una imagen desde URL |
| `/clear` | Limpia el contexto |
| `/history` | Muestra stats de conversación |
| `/exit` | Termina el programa |

## ⚙️ Arquitectura

### Context Manager
**Estrategia:** Sliding Window con priorización
- Mantiene primeros 2 mensajes (contexto inicial)
- Mantiene últimos 4 mensajes (contexto reciente)
- Límite: ~4000 tokens
- Reserva 500 tokens para respuesta del modelo

```python
# Ejemplo de uso
context = ContextManager(max_tokens=4000, reserved_tokens=500)
context.add_message("user", "Hola")
info = context.get_token_info()  # Retorna stats de tokens
```

### OpenAI Service
**Características:**
- Chat Completions API
- Vision API para análisis de imágenes
- Manejo robusto de errores y rate limits
- Validación de URLs de imágenes

```python
# Ejemplo de uso
openai_service = OpenAIService(api_key="sk-...")
response, success = openai_service.chat_completion(messages)
analysis, success = openai_service.analyze_image("https://...")
```

### Token Counter
Usa `tiktoken` para conteo preciso de tokens:

```python
counter = TokenCounter(model="gpt-4")
tokens = counter.count_tokens("texto")
messages_tokens = counter.count_messages_tokens(messages)
```

## 🧪 Ejecución de Tests

```bash
# Ejecutar todos los tests
python3 -m unittest discover -s tests -p "test_*.py" -v

# Tests específicos
python3 -m unittest tests.test_context_manager -v
python3 -m unittest tests.test_token_counter -v
```

## ⚠️ Manejo de Errores

El chatbot maneja automáticamente:

- **Rate Limits**: Espera inteligente y reintentos
- **Timeouts**: Mensajes de error con sugerencia
- **URLs Inválidas**: Validación antes de enviar a API
- **Conexión**: Manejo de errores de red
- **Tokens Overflow**: Estrategia de sliding window

## 🔐 Seguridad

- ✅ Nunca commitear `.env` (usar `.env.example`)
- ✅ API Key en variables de entorno
- ✅ Validación de entrada del usuario
- ✅ Timeouts configurables

## 📊 Performance

- Token counting: ~0.1ms por mensaje
- API call: ~1-3s (depende de OpenAI)
- Context management: O(n) donde n = mensajes

## 🛠️ Troubleshooting

### "OPENAI_API_KEY no está configurada"
```bash
# Verificar .env existe y tiene la key
cat .env
# Asegúrate de que esté después de:
source venv/bin/activate
```

### "ImportError: No module named 'openai'"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Rate Limit Error
```
El bot esperará automáticamente. Si persiste:
- Aguarda 1 minuto
- Verifica tu plan de OpenAI
- Considera usar GPT-3.5 en lugar de GPT-4
```

## 🎓 Conceptos Implementados

1. **Arquitectura Modular**: Separación clara de responsabilidades
2. **State Management**: Contexto persistente con límite de tokens
3. **Error Handling**: Manejo robusto de múltiples tipos de error
4. **API Integration**: Uso de OpenAI Chat + Vision APIs
5. **Token Optimization**: Estrategia eficiente de gestión de contexto
6. **Testing**: Cobertura de módulos core

## 📝 Notas

- El modelo por defecto es `gpt-4`. Puede cambiar a `gpt-3.5-turbo` en `.env`
- El timeout está en 30 segundos. Ajustar según necesidad
- El contexto máximo es ~4000 tokens. Configurable en `.env`

## 📄 Licencia

Proyecto de ejemplo - Uso educativo
