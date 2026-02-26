#!/usr/bin/env python3
"""
NanoClaw - Ultra-extensible AI Assistant
Usage:
    python main.py                  # Interactive chat
    python main.py -m "your msg"    # Single message
    python main.py --init           # Setup wizard
    python main.py --list-skills    # Show loaded skills
"""

import argparse
import json
import os
import sys


CONFIG_PATH = os.path.expanduser("~/.nanoclaw/config.json")


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        print("⚙️  NanoClaw no está configurado todavía.")
        print("   Ejecuta: python main.py --init\n")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def ask(question: str, default: str = "") -> str:
    prompt = f"{question} [{default}]: " if default else f"{question}: "
    answer = input(prompt).strip()
    return answer if answer else default


def ask_yes_no(question: str, default: bool = True) -> bool:
    hint = "(S/n)" if default else "(s/N)"
    answer = input(f"{question} {hint}: ").strip().lower()
    if not answer:
        return default
    return answer in ("s", "si", "sí", "yes", "y")


def ask_choice(question: str, options: list) -> dict:
    print(f"\n{question}")
    for i, opt in enumerate(options, 1):
        tag = " (recomendado)" if opt.get("recommended") else ""
        print(f"  {i}. {opt['label']}{tag}")
        if opt.get("description"):
            print(f"     {opt['description']}")
    while True:
        choice = input(f"\nElige (1-{len(options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"  Por favor elige un número entre 1 y {len(options)}")


def setup_wizard():
    print("\n" + "═" * 50)
    print("  🦐 Bienvenido a NanoClaw!")
    print("  Asistente de configuración")
    print("═" * 50 + "\n")

    config = {}

    # ── PASO 1: Proveedor ────────────────────────
    print("📡 PASO 1 — Proveedor de IA\n")
    print("  NanoClaw necesita una API key para conectarse a un modelo de lenguaje.")
    print("  Recomendamos OpenRouter: es gratuito y da acceso a muchos modelos.")
    print("  👉 Consigue tu key gratis en: https://openrouter.ai/keys\n")

    provider_choice = ask_choice("¿Qué proveedor quieres usar?", [
        {"label": "OpenRouter", "description": "Acceso a cientos de modelos. Tier gratuito disponible.", "value": "openrouter", "recommended": True},
        {"label": "Anthropic (Claude)", "description": "Modelos Claude directamente.", "value": "anthropic"},
        {"label": "OpenAI (ChatGPT)", "description": "Modelos GPT directamente.", "value": "openai"},
        {"label": "Groq", "description": "Muy rápido. Tier gratuito disponible.", "value": "groq"},
    ])

    provider = provider_choice["value"]
    key_urls = {
        "openrouter": "https://openrouter.ai/keys",
        "anthropic": "https://console.anthropic.com",
        "openai": "https://platform.openai.com/api-keys",
        "groq": "https://console.groq.com/keys",
    }

    print(f"\n  👉 Consigue tu key en: {key_urls[provider]}\n")
    while True:
        api_key = ask("  Pega tu API key aquí")
        if api_key and len(api_key) > 10:
            break
        print("  ❌ La key no parece válida. Inténtalo de nuevo.")

    config["providers"] = {provider: {"api_key": api_key}}
    if provider == "openrouter":
        config["providers"][provider]["api_base"] = "https://openrouter.ai/api/v1"
    print("  ✅ API key guardada\n")

    # ── PASO 2: Modelo ───────────────────────────
    print("🤖 PASO 2 — Modelo de IA\n")
    model_options = {
        "openrouter": [
            {"label": "openrouter/auto — Elige automáticamente el mejor disponible", "value": "openrouter/auto", "recommended": True},
            {"label": "openai/gpt-4o-mini — Rápido y barato (requiere créditos)", "value": "openai/gpt-4o-mini"},
            {"label": "anthropic/claude-haiku-4-5 — Muy bueno (requiere créditos)", "value": "anthropic/claude-haiku-4-5-20251001"},
            {"label": "Introducir manualmente", "value": "__manual__"},
        ],
        "anthropic": [
            {"label": "claude-haiku-4-5 — Rápido y eficiente", "value": "claude-haiku-4-5-20251001", "recommended": True},
            {"label": "claude-sonnet-4-6 — Más potente", "value": "claude-sonnet-4-6"},
            {"label": "Introducir manualmente", "value": "__manual__"},
        ],
        "openai": [
            {"label": "gpt-4o-mini — Rápido y barato", "value": "gpt-4o-mini", "recommended": True},
            {"label": "gpt-4o — Más potente", "value": "gpt-4o"},
            {"label": "Introducir manualmente", "value": "__manual__"},
        ],
        "groq": [
            {"label": "llama-3.1-8b-instant — Muy rápido, gratuito", "value": "llama-3.1-8b-instant", "recommended": True},
            {"label": "llama-3.3-70b-versatile — Más potente", "value": "llama-3.3-70b-versatile"},
            {"label": "Introducir manualmente", "value": "__manual__"},
        ],
    }

    model_choice = ask_choice("¿Qué modelo quieres usar?", model_options[provider])
    model = ask("  Escribe el nombre exacto del modelo") if model_choice["value"] == "__manual__" else model_choice["value"]
    config["agent"] = {"model": model, "max_tokens": 4096, "temperature": 0.7}
    print(f"  ✅ Modelo configurado: {model}\n")

    # ── PASO 3: Búsqueda web ─────────────────────
    print("🔍 PASO 3 — Búsqueda web (opcional)\n")
    print("  NanoClaw puede buscar en internet usando Brave Search API.")
    print("  Es gratuito: 2000 búsquedas/mes.")
    print("  👉 Consigue tu key en: https://brave.com/search/api\n")

    config["tools"] = {"web_search": {}}
    if ask_yes_no("¿Quieres activar la búsqueda web?", default=True):
        brave_key = ask("  Pega tu Brave Search API key (Enter para saltar)")
        if brave_key:
            config["tools"]["web_search"]["api_key"] = brave_key
            print("  ✅ Búsqueda web activada\n")
        else:
            print("  ⏭️  Búsqueda web desactivada por ahora\n")
    else:
        print("  ⏭️  Búsqueda web desactivada\n")

    # ── GUARDAR ──────────────────────────────────
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("═" * 50)
    print("  ✅ ¡NanoClaw está listo!")
    print("═" * 50)
    print()
    print("  Para chatear:               python main.py")
    print('  Para un mensaje rápido:     python main.py -m "¿Qué hora es?"')
    print("  Para ver skills:            python main.py --list-skills")
    print()


def main():
    parser = argparse.ArgumentParser(description="NanoClaw - Ultra-extensible AI Assistant")
    parser.add_argument("-m", "--message", help="Enviar un mensaje y salir")
    parser.add_argument("--list-skills", action="store_true", help="Listar skills cargados")
    parser.add_argument("--init", action="store_true", help="Asistente de configuración")
    args = parser.parse_args()

    if args.init:
        setup_wizard()
        return

    config = load_config()
    from core.agent import Agent
    agent = Agent(config)

    if args.list_skills:
        print("\n📦 Skills cargados:")
        for name, skill in agent.skills.items():
            print(f"\n  🔧 {name}")
            print(f"     {skill.description}")
            if skill.args_schema:
                for arg, desc in skill.args_schema.items():
                    print(f"     • {arg}: {desc}")
        return

    if args.message:
        response = agent.chat(args.message)
        print(f"\n{response}")
        return

    print("\n🦐 NanoClaw listo! Escribe tu mensaje (Ctrl+C o 'salir' para terminar, 'reset' para limpiar historial)\n")
    while True:
        try:
            user_input = input("Tú: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("salir", "exit", "quit", "bye"):
                print("👋 ¡Hasta luego!")
                break
            if user_input.lower() == "reset":
                agent.reset_history()
                continue
            response = agent.chat(user_input)
            print(f"\nNanoClaw: {response}\n")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()