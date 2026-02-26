"""
Skill: web_search
Searches the web using Brave Search API (free tier: 2000 queries/month).
Get your key at: https://brave.com/search/api
"""

import os
import requests
from core.base_skill import BaseSkill


class WebSearchSkill(BaseSkill):
    name = "web_search"
    description = "Search the web for current information, news, facts, or any topic."
    args_schema = {
        "query": "The search query to look up on the web",
    }

    def run(self, query: str) -> str:
        api_key = os.getenv("BRAVE_API_KEY") or self._load_from_config()

        if not api_key:
            return (
                "Web search is not configured. "
                "Get a free API key at https://brave.com/search/api "
                "and add it to config.json under tools.web_search.api_key"
            )

        try:
            resp = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "X-Subscription-Token": api_key,
                },
                params={"q": query, "count": 5},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

            results = data.get("web", {}).get("results", [])
            if not results:
                return f"No results found for: {query}"

            formatted = []
            for r in results[:5]:
                formatted.append(
                    f"**{r.get('title', 'No title')}**\n"
                    f"{r.get('url', '')}\n"
                    f"{r.get('description', 'No description')}"
                )

            return "\n\n".join(formatted)

        except requests.RequestException as e:
            return f"Search failed: {e}"

    def _load_from_config(self) -> str | None:
        """Try to read API key from config.json."""
        try:
            import json
            config_path = os.path.expanduser("~/.nanoclaw/config.json")
            if os.path.exists(config_path):
                with open(config_path) as f:
                    config = json.load(f)
                return config.get("tools", {}).get("web_search", {}).get("api_key")
        except Exception:
            pass
        return None