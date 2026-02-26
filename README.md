# 🦐 NanoClaw

> Un asistente de IA ultra-extensible escrito en Python.  
> Inspirado en [PicoClaw](https://github.com/sipeed/picoclaw) — construido para máxima extensibilidad de skills.

## ✨ ¿Qué lo hace diferente?

La filosofía central es **un archivo = un skill**. Añade un `.py` a `/skills` y el agente lo descubre automáticamente. Sin registros, sin configuración extra.

| | PicoClaw | NanoClaw |
|---|---|---|
| Lenguaje | Go | Python |
| Sistema de skills | Integrado | 🔌 Modular, plug-and-play |
| Añadir un skill | Modificar el core | Solo añadir un archivo a `/skills` |
| Ecosistema | Mínimo | Todo el ecosistema Python |

---

## 🚀 Instalación y configuración

### 1. Clona el repositorio

```bash
git clone https://github.com/YOUR_USERNAME/nanoclaw
cd nanoclaw
pip install -r requirements.txt
```

### 2. Ejecuta el asistente de configuración

```bash
python main.py --init
```

El asistente te guiará paso a paso:

```
══════════════════════════════════════════════════
  🦐 Bienvenido a NanoClaw!
  Asistente de configuración
══════════════════════════════════════════════════

📡 PASO 1 — Proveedor de IA
  👉 Consigue tu key gratis en: https://openrouter.ai/keys

  ¿Qué proveedor quieres usar?
  1. OpenRouter (recomendado)
     Acceso a cientos de modelos. Tier gratuito disponible.
  2. Anthropic (Claude)
  3. OpenAI (ChatGPT)
  4. Groq

🤖 PASO 2 — Modelo de IA
  1. openrouter/auto — Elige automáticamente el mejor disponible (recomendado)
  2. openai/gpt-4o-mini — Rápido y barato
  ...

🔍 PASO 3 — Búsqueda web (opcional)
  👉 Consigue tu key en: https://brave.com/search/api

✅ ¡NanoClaw está listo!
```

### 3. ¡Úsalo!

```bash
python main.py                        # Modo conversación
python main.py -m "¿Qué hora es?"    # Mensaje rápido
python main.py --list-skills          # Ver skills disponibles
```

---

## 🔑 API Keys necesarias

| Servicio | Para qué | Tier gratuito | Enlace |
|---|---|---|---|
| **OpenRouter** | Modelo de IA (obligatorio) | 200K tokens/mes | [openrouter.ai/keys](https://openrouter.ai/keys) |
| **Brave Search** | Búsqueda web (opcional) | 2000 búsquedas/mes | [brave.com/search/api](https://brave.com/search/api) |

---

## 📦 Skills incluidos

| Skill | Descripción |
|---|---|
| `web_search` | Búsqueda web via Brave Search API |
| `file_manager` | Leer, escribir, listar y borrar archivos en tu workspace |
| `code_runner` | Ejecutar código Python y expresiones matemáticas |
| `task_manager` | Lista de tareas personal que persiste entre sesiones |
| `system_info` | Fecha/hora, info del OS, uso de disco |

---

## 🔧 Cómo añadir un nuevo skill

Crea un archivo en `/skills/`. Eso es todo.

```python
# skills/mi_skill.py
from core.base_skill import BaseSkill

class MiSkill(BaseSkill):
    name = "mi_skill"
    description = "Hace algo útil"
    args_schema = {
        "input": "El texto a procesar"
    }

    def run(self, input: str) -> str:
        return f"Resultado: {input}"
```

El agente lo descarga y carga en el próximo arranque sin tocar nada más.

---

## 🗺️ Roadmap

- [ ] Canal Telegram
- [ ] Canal Discord
- [ ] Skill de memoria / notas largas
- [ ] Skill de clima
- [ ] Skill de email (Gmail API)
- [ ] Skill de calendario (Google Calendar)
- [ ] Skill de resumen de URLs
- [ ] Skill de generación de imágenes

## 🤝 Contribuir

Los PRs son bienvenidos. El código es intencionalmente pequeño y legible.  
Lee [CONTRIBUTING.md](docs/CONTRIBUTING.md) antes de empezar.

## 📄 Licencia

MIT
