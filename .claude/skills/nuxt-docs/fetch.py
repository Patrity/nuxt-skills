#!/usr/bin/env python3
"""
Nuxt 4 Documentation Fetcher

Fetches Nuxt framework docs from the official GitHub repository.

Usage:
    python fetch.py <topic>           # Fetch specific topic
    python fetch.py <topic> --force   # Force refresh
    python fetch.py --list            # List available topics
    python fetch.py --status          # Show cache status
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CACHE_DIR = SCRIPT_DIR / "cache"
MANIFEST_PATH = SCRIPT_DIR / "manifest.json"

GITHUB_RAW = "https://raw.githubusercontent.com"
REPO = "nuxt/nuxt"
BRANCH = "main"
DOCS_PATH = "docs"

CACHE_TTL_HOURS = 24

# Topic to file path mapping
TOPICS = {
    # Getting Started
    "introduction": "1.getting-started/01.introduction.md",
    "installation": "1.getting-started/02.installation.md",
    "configuration": "1.getting-started/03.configuration.md",
    "views": "1.getting-started/04.views.md",
    "assets": "1.getting-started/05.assets.md",
    "styling": "1.getting-started/06.styling.md",
    "routing": "1.getting-started/07.routing.md",
    "seo": "1.getting-started/08.seo-meta.md",
    "seo-meta": "1.getting-started/08.seo-meta.md",
    "transitions": "1.getting-started/09.transitions.md",
    "data-fetching": "1.getting-started/10.data-fetching.md",
    "datafetching": "1.getting-started/10.data-fetching.md",
    "state": "1.getting-started/11.state-management.md",
    "state-management": "1.getting-started/11.state-management.md",
    "error-handling": "1.getting-started/12.error-handling.md",
    "server": "1.getting-started/13.server.md",
    "layers": "1.getting-started/14.layers.md",
    "prerendering": "1.getting-started/15.prerendering.md",
    "deployment": "1.getting-started/16.deployment.md",
    "testing": "1.getting-started/17.testing.md",
    "upgrade": "1.getting-started/18.upgrade.md",

    # Directory Structure
    "directory": "2.directory-structure/0.index.md",
    "directory-structure": "2.directory-structure/0.index.md",
    "nuxtconfig": "2.directory-structure/1.nuxt-config.md",
    "nuxt-config": "2.directory-structure/1.nuxt-config.md",
    "appconfig": "2.directory-structure/2.app-config.md",
    "app-config": "2.directory-structure/2.app-config.md",
    "app-vue": "2.directory-structure/3.app-vue.md",

    # API - Composables
    "usefetch": "4.api/2.composables/use-fetch.md",
    "useasyncdata": "4.api/2.composables/use-async-data.md",
    "usestate": "4.api/2.composables/use-state.md",
    "useroute": "4.api/2.composables/use-route.md",
    "userouter": "4.api/2.composables/use-router.md",
    "useHead": "4.api/2.composables/use-head.md",
    "usehead": "4.api/2.composables/use-head.md",
    "useseoMeta": "4.api/2.composables/use-seo-meta.md",
    "useseometa": "4.api/2.composables/use-seo-meta.md",
    "useruntimeconfig": "4.api/2.composables/use-runtime-config.md",
    "useappconfig": "4.api/2.composables/use-app-config.md",
    "usenuxtapp": "4.api/2.composables/use-nuxt-app.md",
    "uselazyfetch": "4.api/2.composables/use-lazy-fetch.md",
    "uselazyasyncdata": "4.api/2.composables/use-lazy-async-data.md",
    "usecookie": "4.api/2.composables/use-cookie.md",
    "userequesturl": "4.api/2.composables/use-request-url.md",

    # API - Components
    "nuxtpage": "4.api/1.components/nuxt-page.md",
    "nuxtlayout": "4.api/1.components/nuxt-layout.md",
    "nuxtlink": "4.api/1.components/nuxt-link.md",
    "clientonly": "4.api/1.components/client-only.md",
    "nuxtimg": "4.api/1.components/nuxt-img.md",
    "nuxtpicture": "4.api/1.components/nuxt-picture.md",

    # API - Utils
    "$fetch": "4.api/3.utils/$fetch.md",
    "fetch": "4.api/3.utils/$fetch.md",
    "definenuxtconfig": "4.api/3.utils/define-nuxt-config.md",
    "definepagemeta": "4.api/3.utils/define-page-meta.md",
    "defineeventhandler": "4.api/3.utils/define-event-handler.md",
    "navigateto": "4.api/3.utils/navigate-to.md",

    # Nuxt Config reference
    "config": "4.api/6.nuxt-config.md",
    "nuxt.config": "4.api/6.nuxt-config.md",
}


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH) as f:
            return json.load(f)
    return {"topics": {}}


def save_manifest(manifest: dict) -> None:
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)


def fetch_url(url: str) -> str | None:
    try:
        result = subprocess.run(
            ["curl", "-sL", "-H", "User-Agent: Claude-Code-Nuxt-Docs", url],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0 and result.stdout and len(result.stdout) > 50:
            if "404" in result.stdout[:200] and "Not Found" in result.stdout[:200]:
                return None
            return result.stdout
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def is_cache_valid(topic: str, manifest: dict, force: bool = False) -> bool:
    if force:
        return False
    topic_data = manifest.get("topics", {}).get(topic.lower())
    if not topic_data:
        return False
    cached_file = CACHE_DIR / f"{topic.lower()}.md"
    if not cached_file.exists():
        return False
    last_fetch = datetime.fromisoformat(topic_data["last_fetch"])
    age = datetime.now() - last_fetch
    return age < timedelta(hours=CACHE_TTL_HOURS)


def fetch_topic(topic: str, force: bool = False) -> str | None:
    manifest = load_manifest()
    topic_lower = topic.lower()

    if is_cache_valid(topic_lower, manifest, force):
        cached_file = CACHE_DIR / f"{topic_lower}.md"
        print(f"Using cached docs for {topic} (use --force to refresh)", file=sys.stderr)
        return cached_file.read_text()

    doc_path = TOPICS.get(topic_lower)
    if not doc_path:
        # Try to find a matching file
        print(f"Unknown topic: {topic}", file=sys.stderr)
        print("Use --list to see available topics", file=sys.stderr)
        return None

    url = f"{GITHUB_RAW}/{REPO}/{BRANCH}/{DOCS_PATH}/{doc_path}"
    print(f"Fetching: {url}", file=sys.stderr)

    content = fetch_url(url)
    if content:
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / f"{topic_lower}.md"
        cache_file.write_text(content)

        manifest.setdefault("topics", {})[topic_lower] = {
            "last_fetch": datetime.now().isoformat(),
            "source_path": doc_path,
        }
        save_manifest(manifest)
        return content

    return None


def list_topics() -> None:
    print("=== Available Nuxt Documentation Topics ===\n")

    categories = {
        "Getting Started": [
            "introduction", "installation", "configuration", "views", "assets",
            "styling", "routing", "seo-meta", "transitions", "data-fetching",
            "state-management", "error-handling", "server", "layers",
            "prerendering", "deployment", "testing", "upgrade"
        ],
        "Directory Structure": [
            "directory-structure", "nuxt-config", "app-config", "app-vue"
        ],
        "Composables": [
            "usefetch", "useasyncdata", "usestate", "useroute", "userouter",
            "usehead", "useseometa", "useruntimeconfig", "useappconfig",
            "usenuxtapp", "uselazyfetch", "uselazyasyncdata", "usecookie"
        ],
        "Components": [
            "nuxtpage", "nuxtlayout", "nuxtlink", "clientonly"
        ],
        "Utils": [
            "$fetch", "definenuxtconfig", "definepagemeta", "defineeventhandler",
            "navigateto"
        ],
        "Config": ["config"],
    }

    for category, topics in categories.items():
        print(f"{category}:")
        for t in topics:
            print(f"  - {t}")
        print()


def show_status() -> None:
    manifest = load_manifest()
    topics = manifest.get("topics", {})

    print("=== Nuxt Docs Cache Status ===\n")
    print(f"Cache TTL: {CACHE_TTL_HOURS} hours\n")

    if not topics:
        print("No topics cached yet.")
        return

    print(f"Cached topics ({len(topics)}):\n")
    for name, data in sorted(topics.items()):
        last_fetch = datetime.fromisoformat(data["last_fetch"])
        age = datetime.now() - last_fetch
        hours = age.total_seconds() / 3600
        status = "fresh" if hours < CACHE_TTL_HOURS else "stale"
        print(f"  {name:20} {status:6} ({hours:.1f}h ago)")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    if args[0] == "--list":
        list_topics()
    elif args[0] == "--status":
        show_status()
    else:
        topic = args[0]
        force = "--force" in args
        content = fetch_topic(topic, force)
        if content:
            print(f"\n# {topic}\n")
            print(content)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
