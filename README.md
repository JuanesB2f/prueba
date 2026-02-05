
```md
#  Chatbot Conversacional CLI con OpenAI

Chatbot por línea de comandos (CLI) que mantiene contexto conversacional, analiza imágenes desde URLs públicas y gestiona automáticamente el límite de tokens.

---

## 🎯 Funcionalidad

- Chat conversacional con memoria
- Análisis de imágenes vía OpenAI Vision
- Gestión de contexto con sliding window
- Comandos de sistema
- Arquitectura modular y mantenible

---

##  Arquitectura

```

src/
├── main.py              # Punto de entrada
├── chatbot.py           # Loop principal
├── context_manager.py   # Gestión de contexto y tokens
├── openai_service.py    # OpenAI Chat + Vision
├── command_handler.py   # Comandos CLI
├── config.py            # Configuración (.env)
└── exceptions.py        # Excepciones

```

---

##  Gestión de Contexto

Se implementa una estrategia de **sliding window**:

- Se mantiene siempre el mensaje del sistema
- Se conservan los últimos *N* mensajes
- Al superar el límite de tokens (~4000), el contexto se recorta automáticamente

Esto prioriza relevancia reciente y evita errores de contexto.

---

##  Análisis de Imágenes

El comando `/imagen <url>`:

- Analiza la imagen **una sola vez**
- Guarda la descripción en el contexto
- Permite preguntas posteriores sin reenviar la imagen

Ejemplo:
```

> /imagen [https://upload.wikimedia.org/](https://upload.wikimedia.org/)...
> < Bot: En la imagen se observa...
> ¿De qué color es el objeto?
> < Bot: Según la imagen analizada previamente...

````

---

##  Instalación

```bash
pip install -r requirements.txt
````

### Configurar `.env`

```env
OPENAI_API_KEY=tu_api_key
```

>  No incluir `.env` en el repositorio por seguridad.

---

##  Uso

```bash
python src/main.py
```

---

##  Comandos propuestos

| Comando         | Descripción              |
| --------------- | ------------------------ |
| `/help`         | Muestra comandos         |
| `/imagen <url>` | Analiza imagen           |
| `/clear`        | Limpia el contexto       |
| `/history`      | Información del contexto |
| `/exit`         | Salir                    |

---


El chatbot no se bloquea ante errores.

---

##  Tecnologías

* Python 3.8+
* OpenAI SDK
* tiktoken
* python-dotenv

---

##  Notas

* Las imágenes deben ser URLs directas (`.jpg`, `.png`, etc.)
* Proyecto enfocado en arquitectura y manejo de contexto
* Pensado para evaluación técnica senior

```
