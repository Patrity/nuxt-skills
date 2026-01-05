#!/usr/bin/env python3
"""
Nuxt UI Templates Fetcher

Fetches real implementation examples from the nuxt-ui-templates GitHub org.

Usage:
    python fetch.py --list                           # List available templates
    python fetch.py dashboard --structure            # Show template file structure
    python fetch.py dashboard app/layouts/default.vue   # Fetch specific file
    python fetch.py dashboard --search "Sidebar"     # Search for patterns
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CACHE_DIR = SCRIPT_DIR / "cache"

GITHUB_API = "https://api.github.com"
GITHUB_RAW = "https://raw.githubusercontent.com"
ORG = "nuxt-ui-templates"

# Available templates with their descriptions and key files
TEMPLATES = {
    "dashboard": {
        "description": "Full dashboard with sidebar, panels, navbar",
        "branch": "main",
        "key_files": [
            "app/layouts/default.vue",
            "app/app.vue",
            "app/composables/useDashboard.ts",
            "app/pages/index.vue",
            "app/pages/inbox.vue",
            "app/components/inbox/InboxList.vue",
        ]
    },
    "saas": {
        "description": "SaaS app with auth, pricing, landing",
        "branch": "main",
        "key_files": [
            "app/pages/pricing.vue",
            "app/pages/index.vue",
            "app/layouts/default.vue",
        ]
    },
    "landing": {
        "description": "Marketing landing page",
        "branch": "main",
        "key_files": [
            "app/pages/index.vue",
            "app/components/Hero.vue",
        ]
    },
    "chat": {
        "description": "AI chatbot with Vercel AI SDK",
        "branch": "main",
        "key_files": [
            "app/pages/index.vue",
            "app/components/Chat.vue",
        ]
    },
    "docs": {
        "description": "Documentation site",
        "branch": "main",
        "key_files": [
            "app/layouts/docs.vue",
            "app/pages/index.vue",
        ]
    },
    "portfolio": {
        "description": "Portfolio/personal site",
        "branch": "main",
        "key_files": [
            "app/pages/index.vue",
        ]
    },
    "editor": {
        "description": "Notion-like WYSIWYG editor",
        "branch": "main",
        "key_files": [
            "app/pages/index.vue",
            "app/components/Editor.vue",
        ]
    },
    "changelog": {
        "description": "Changelog/release notes",
        "branch": "main",
        "key_files": [
            "app/pages/index.vue",
        ]
    },
    "starter": {
        "description": "Minimal Nuxt UI starter",
        "branch": "main",
        "key_files": [
            "app/app.vue",
            "nuxt.config.ts",
        ]
    },
}


def fetch_url(url: str) -> str | None:
    """Fetch content from URL using curl."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "-H", "User-Agent: Claude-Code-Nuxt-Templates", url],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0 and result.stdout:
            if "404" in result.stdout[:200] and "Not Found" in result.stdout[:200]:
                return None
            return result.stdout
        return None
    except subprocess.TimeoutExpired:
        print(f"Timeout fetching {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def list_templates() -> None:
    """List available templates."""
    print("=== Available Nuxt UI Templates ===\n")
    for name, info in TEMPLATES.items():
        print(f"  {name:12} - {info['description']}")
    print("\nUsage: python fetch.py <template> --structure")
    print("       python fetch.py <template> <file_path>")


def get_tree(template: str, path: str = "") -> list[dict] | None:
    """Get directory tree from GitHub API."""
    info = TEMPLATES.get(template)
    if not info:
        return None

    branch = info["branch"]
    url = f"{GITHUB_API}/repos/{ORG}/{template}/git/trees/{branch}?recursive=1"
    content = fetch_url(url)

    if content:
        try:
            data = json.loads(content)
            return data.get("tree", [])
        except json.JSONDecodeError:
            return None
    return None


def show_structure(template: str) -> None:
    """Show the file structure of a template."""
    tree = get_tree(template)
    if not tree:
        print(f"Could not fetch structure for template: {template}")
        return

    print(f"=== {template} Template Structure ===\n")

    # Filter to relevant directories
    relevant_dirs = ["app/", "components/", "layouts/", "pages/", "composables/", "server/"]

    for item in tree:
        path = item["path"]
        item_type = item["type"]

        # Only show relevant paths
        if any(path.startswith(d) or path.endswith(('.vue', '.ts', '.js')) for d in relevant_dirs):
            if item_type == "blob":
                # It's a file
                indent = "  " * (path.count("/"))
                print(f"{indent}{path}")

    print(f"\nKey files for {template}:")
    for f in TEMPLATES[template].get("key_files", []):
        print(f"  - {f}")


def fetch_file(template: str, file_path: str) -> str | None:
    """Fetch a specific file from a template."""
    info = TEMPLATES.get(template)
    if not info:
        print(f"Unknown template: {template}", file=sys.stderr)
        return None

    branch = info["branch"]
    url = f"{GITHUB_RAW}/{ORG}/{template}/{branch}/{file_path}"
    print(f"Fetching: {url}", file=sys.stderr)

    content = fetch_url(url)
    if content:
        # Cache it
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / f"{template}_{file_path.replace('/', '_')}"
        cache_file.write_text(content)
        return content

    return None


def search_template(template: str, query: str) -> None:
    """Search for a pattern in template files."""
    tree = get_tree(template)
    if not tree:
        print(f"Could not fetch tree for template: {template}")
        return

    print(f"=== Searching '{query}' in {template} ===\n")

    matches = []
    for item in tree:
        if item["type"] == "blob" and item["path"].endswith(('.vue', '.ts', '.js')):
            content = fetch_file(template, item["path"])
            if content and query.lower() in content.lower():
                matches.append(item["path"])

    if matches:
        print(f"Found in {len(matches)} files:")
        for m in matches:
            print(f"  - {m}")
        print(f"\nFetch with: python fetch.py {template} <file_path>")
    else:
        print(f"No matches found for '{query}'")


def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] == "--list":
        list_templates()
        return

    template = args[0]

    if template not in TEMPLATES:
        print(f"Unknown template: {template}")
        print("Use --list to see available templates")
        sys.exit(1)

    if len(args) == 1:
        # Just template name - show structure
        show_structure(template)
        return

    if args[1] == "--structure":
        show_structure(template)
    elif args[1] == "--search" and len(args) > 2:
        search_template(template, args[2])
    else:
        # Assume it's a file path
        file_path = args[1]
        content = fetch_file(template, file_path)
        if content:
            print(f"\n# {template}/{file_path}\n")
            print(content)
        else:
            print(f"Could not fetch file: {file_path}")
            print(f"\nUse: python fetch.py {template} --structure")
            sys.exit(1)


if __name__ == "__main__":
    main()
