# 🤖 NanoClaw

> An ultra-extensible AI assistant written in Python.  
> Inspired by [PicoClaw](https://github.com/sipeed/picoclaw) — built for maximum skill extensibility.

## ✨ What makes it different?

The core philosophy is **one file = one skill**. Drop a `.py` file in `/skills` and the agent discovers it automatically. No configuration needed.

| Feature | PicoClaw | NanoClaw |
|---|---|---|
| Language | Go | Python |
| Skills system | Built-in | 🔌 Fully modular, plug-and-play |
| Adding skills | Modify core | Just add a file to `/skills` |
| Ecosystem | Minimal | Full Python ecosystem |

## 🚀 Quick Start

### 1. Install
```bash
git clone https://github.com/YOUR_USERNAME/nanoclaw
cd nanoclaw
pip install -r requirements.txt
```

### 2. Configure
```bash
python main.py --init
# Then edit ~/.nanoclaw/config.json with your API keys
```

Get free API keys:
- **LLM**: [OpenRouter](https://openrouter.ai/keys) — 200K tokens/month free
- **Search**: [Brave Search API](https://brave.com/search/api) — 2000 queries/month free

### 3. Run
```bash
python main.py                   # Interactive mode
python main.py -m "What time is it?"  # Single message
python main.py --list-skills     # See all skills
```

## 📦 Built-in Skills

| Skill | Description |
|---|---|
| `web_search` | Search the web via Brave Search API |
| `file_manager` | Read, write, list, delete files in your workspace |
| `code_runner` | Execute Python code and math expressions |
| `task_manager` | Personal to-do list that persists between sessions |
| `system_info` | Date/time, OS info, disk usage |

## 🔧 Adding a New Skill

Create a file in `/skills/`. That's it.

```python
# skills/my_skill.py
from core.base_skill import BaseSkill

class MySkill(BaseSkill):
    name = "my_skill"
    description = "Does something awesome"
    args_schema = {
        "input": "The input to process"
    }

    def run(self, input: str) -> str:
        return f"Processed: {input}"
```

The agent will discover and load it on next startup.

## 🗺️ Roadmap

- [ ] Telegram channel integration
- [ ] Discord channel integration  
- [ ] Memory / long-term notes skill
- [ ] Weather skill
- [ ] Email skill (via Gmail API)
- [ ] Calendar skill (via Google Calendar)
- [ ] RSS/news reader skill
- [ ] URL summarizer skill
- [ ] Image generation skill

## 🤝 Contributing

PRs welcome! The codebase is intentionally small and readable.  
Read [CONTRIBUTING.md](docs/CONTRIBUTING.md) before starting.

## 📄 License

MIT
