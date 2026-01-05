#!/usr/bin/env python3
"""
Nuxt UI v4 Documentation Fetcher

Fetches and caches Nuxt UI component docs from GitHub.
Tracks updates via manifest.json to avoid redundant fetches.

Usage:
    python fetch.py Button              # Fetch Button component docs
    python fetch.py Button --force      # Force refresh, bypass cache
    python fetch.py --update-all        # Update all cached components
    python fetch.py --status            # Show cache status
    python fetch.py --list              # List available components
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CACHE_DIR = SCRIPT_DIR / "cache"
MANIFEST_PATH = SCRIPT_DIR / "manifest.json"

GITHUB_API = "https://api.github.com"
GITHUB_RAW = "https://raw.githubusercontent.com"
REPO = "nuxt/ui"
BRANCH = "v4"
DOCS_PATH = "docs/content/docs/2.components"

# Cache validity period (hours)
CACHE_TTL_HOURS = 24

# Known component paths in Nuxt UI v4 docs (relative to DOCS_PATH)
# Auto-generated from GitHub repo
COMPONENT_PATHS = {
    # Form
    "button": "button.md",
    "checkbox": "checkbox.md",
    "checkboxgroup": "checkbox-group.md",
    "colorpicker": "color-picker.md",
    "fileupload": "file-upload.md",
    "form": "form.md",
    "formfield": "form-field.md",
    "fieldgroup": "field-group.md",
    "input": "input.md",
    "inputdate": "input-date.md",
    "inputmenu": "input-menu.md",
    "inputnumber": "input-number.md",
    "inputtags": "input-tags.md",
    "inputtime": "input-time.md",
    "pinput": "pin-input.md",
    "radiogroup": "radio-group.md",
    "select": "select.md",
    "selectmenu": "select-menu.md",
    "slider": "slider.md",
    "switch": "switch.md",
    "textarea": "textarea.md",
    "authform": "auth-form.md",

    # Data
    "accordion": "accordion.md",
    "calendar": "calendar.md",
    "carousel": "carousel.md",
    "table": "table.md",
    "tree": "tree.md",
    "timeline": "timeline.md",

    # Navigation
    "breadcrumb": "breadcrumb.md",
    "commandpalette": "command-palette.md",
    "pagination": "pagination.md",
    "stepper": "stepper.md",
    "tabs": "tabs.md",

    # Overlays
    "contextmenu": "context-menu.md",
    "drawer": "drawer.md",
    "dropdownmenu": "dropdown-menu.md",
    "modal": "modal.md",
    "popover": "popover.md",
    "slideover": "slideover.md",
    "tooltip": "tooltip.md",

    # Feedback
    "alert": "alert.md",
    "badge": "badge.md",
    "banner": "banner.md",
    "empty": "empty.md",
    "error": "error.md",
    "progress": "progress.md",
    "skeleton": "skeleton.md",
    "toast": "toast.md",

    # Layout
    "app": "app.md",
    "card": "card.md",
    "container": "container.md",
    "main": "main.md",
    "scrollarea": "scroll-area.md",
    "separator": "separator.md",

    # Media
    "avatar": "avatar.md",
    "avatargroup": "avatar-group.md",
    "chip": "chip.md",
    "collapsible": "collapsible.md",
    "icon": "icon.md",
    "kbd": "kbd.md",
    "link": "link.md",
    "user": "user.md",
    "marquee": "marquee.md",

    # Color Mode
    "colormodeavatar": "color-mode-avatar.md",
    "colormodebutton": "color-mode-button.md",
    "colormodeimage": "color-mode-image.md",
    "colormodeselect": "color-mode-select.md",
    "colormodeswitch": "color-mode-switch.md",
    "localeselect": "locale-select.md",

    # Dashboard
    "dashboardgroup": "dashboard-group.md",
    "dashboardnavbar": "dashboard-navbar.md",
    "dashboardpanel": "dashboard-panel.md",
    "dashboardresizehandle": "dashboard-resize-handle.md",
    "dashboardsearchbutton": "dashboard-search-button.md",
    "dashboardsearch": "dashboard-search.md",
    "dashboardsidebarcollapse": "dashboard-sidebar-collapse.md",
    "dashboardsidebartoggle": "dashboard-sidebar-toggle.md",
    "dashboardsidebar": "dashboard-sidebar.md",
    "dashboardtoolbar": "dashboard-toolbar.md",

    # Page
    "page": "page.md",
    "pageanchors": "page-anchors.md",
    "pageaside": "page-aside.md",
    "pagebody": "page-body.md",
    "pagecard": "page-card.md",
    "pagecolumns": "page-columns.md",
    "pagecta": "page-cta.md",
    "pagefeature": "page-feature.md",
    "pagegrid": "page-grid.md",
    "pageheader": "page-header.md",
    "pagehero": "page-hero.md",
    "pagelinks": "page-links.md",
    "pagelist": "page-list.md",
    "pagelogos": "page-logos.md",
    "pagesection": "page-section.md",

    # Header/Footer
    "header": "header.md",
    "footer": "footer.md",
    "footercolumns": "footer-columns.md",

    # Blog
    "blogpost": "blog-post.md",
    "blogposts": "blog-posts.md",

    # Changelog
    "changelogversion": "changelog-version.md",
    "changelogversions": "changelog-versions.md",

    # Chat
    "chatmessage": "chat-message.md",
    "chatmessages": "chat-messages.md",
    "chatpalette": "chat-palette.md",
    "chatprompt": "chat-prompt.md",
    "chatpromptsubmit": "chat-prompt-submit.md",

    # Editor
    "editor": "editor.md",
    "editordraghandle": "editor-drag-handle.md",
    "editoremojimenu": "editor-emoji-menu.md",
    "editormentionmenu": "editor-mention-menu.md",
    "editorsuggestionmenu": "editor-suggestion-menu.md",
    "editortoolbar": "editor-toolbar.md",

    # Content
    "contentsearchbutton": "content-search-button.md",
    "contentsearch": "content-search.md",
    "contentsurround": "content-surround.md",
    "contenttoc": "content-toc.md",

    # Pricing
    "pricingplan": "pricing-plan.md",
    "pricingplans": "pricing-plans.md",
    "pricingtable": "pricing-table.md",
}


def load_manifest() -> dict:
    """Load the manifest file."""
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH) as f:
            return json.load(f)
    return {
        "source": f"https://github.com/{REPO}",
        "branch": BRANCH,
        "docs_path": DOCS_PATH,
        "last_full_update": None,
        "last_commit_sha": None,
        "components": {}
    }


def save_manifest(manifest: dict) -> None:
    """Save the manifest file."""
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)


def fetch_url(url: str) -> str | None:
    """Fetch content from URL using curl."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "-H", "User-Agent: Claude-Code-Nuxt-UI-Docs", url],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0 and result.stdout and len(result.stdout) > 50:
            # Check for 404 page content
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


def get_latest_commit() -> str | None:
    """Get the latest commit SHA for the v4 branch."""
    url = f"{GITHUB_API}/repos/{REPO}/commits/{BRANCH}"
    content = fetch_url(url)
    if content:
        data = json.loads(content)
        return data.get("sha")
    return None


def is_cache_valid(component: str, manifest: dict, force: bool = False) -> bool:
    """Check if cached component is still valid."""
    if force:
        return False

    comp_data = manifest.get("components", {}).get(component.lower())
    if not comp_data:
        return False

    cached_file = CACHE_DIR / f"{component.lower()}.md"
    if not cached_file.exists():
        return False

    last_fetch = datetime.fromisoformat(comp_data["last_fetch"])
    age = datetime.now() - last_fetch

    return age < timedelta(hours=CACHE_TTL_HOURS)


def fetch_component(component: str, force: bool = False) -> str | None:
    """Fetch a component's documentation."""
    manifest = load_manifest()
    comp_lower = component.lower()

    # Check cache
    if is_cache_valid(comp_lower, manifest, force):
        cached_file = CACHE_DIR / f"{comp_lower}.md"
        print(f"Using cached docs for {component} (use --force to refresh)", file=sys.stderr)
        return cached_file.read_text()

    # Find the docs path
    doc_path = COMPONENT_PATHS.get(comp_lower)
    if not doc_path:
        # Try common patterns: component.md or component-name.md
        doc_path = f"{comp_lower}.md"

    url = f"{GITHUB_RAW}/{REPO}/{BRANCH}/{DOCS_PATH}/{doc_path}"
    print(f"Fetching: {url}", file=sys.stderr)

    content = fetch_url(url)
    if not content:
        # Try with hyphenated name (e.g., formfield -> form-field)
        hyphenated = comp_lower.replace("field", "-field").replace("menu", "-menu").replace("group", "-group")
        if hyphenated != comp_lower:
            url = f"{GITHUB_RAW}/{REPO}/{BRANCH}/{DOCS_PATH}/{hyphenated}.md"
            print(f"Trying: {url}", file=sys.stderr)
            content = fetch_url(url)

    if content:
        # Cache the content
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / f"{comp_lower}.md"
        cache_file.write_text(content)

        # Update manifest
        manifest["components"][comp_lower] = {
            "last_fetch": datetime.now().isoformat(),
            "source_path": doc_path,
            "cached_file": str(cache_file.relative_to(SCRIPT_DIR))
        }

        # Update commit SHA
        commit = get_latest_commit()
        if commit:
            manifest["last_commit_sha"] = commit

        save_manifest(manifest)
        print(f"Cached: {cache_file}", file=sys.stderr)
        return content

    return None


def show_status() -> None:
    """Show cache status."""
    manifest = load_manifest()

    print("=== Nuxt UI Docs Cache Status ===\n")
    print(f"Source: {manifest['source']}")
    print(f"Branch: {manifest['branch']}")
    print(f"Last commit SHA: {manifest.get('last_commit_sha', 'unknown')}")
    print(f"Cache TTL: {CACHE_TTL_HOURS} hours\n")

    components = manifest.get("components", {})
    if not components:
        print("No components cached yet.")
        return

    print(f"Cached components ({len(components)}):\n")
    for name, data in sorted(components.items()):
        last_fetch = datetime.fromisoformat(data["last_fetch"])
        age = datetime.now() - last_fetch
        hours = age.total_seconds() / 3600
        status = "fresh" if hours < CACHE_TTL_HOURS else "stale"
        print(f"  {name:20} {status:6} ({hours:.1f}h ago)")


def update_all(force: bool = False) -> None:
    """Update all cached components."""
    manifest = load_manifest()
    components = list(manifest.get("components", {}).keys())

    if not components:
        print("No components cached yet. Fetch individual components first.")
        return

    print(f"Updating {len(components)} cached components...\n")

    for comp in components:
        content = fetch_component(comp, force=force)
        if content:
            print(f"  Updated: {comp}")
        else:
            print(f"  Failed: {comp}")

    # Update full update timestamp
    manifest = load_manifest()
    manifest["last_full_update"] = datetime.now().isoformat()
    save_manifest(manifest)

    print(f"\nDone. Manifest updated.")


def list_components() -> None:
    """List available components."""
    print("=== Available Nuxt UI v4 Components ===\n")

    categories = {
        "Form": ["button", "checkbox", "checkboxgroup", "colorpicker", "fileupload", "form",
                 "formfield", "fieldgroup", "input", "inputdate", "inputmenu", "inputnumber",
                 "inputtags", "inputtime", "pinput", "radiogroup", "select", "selectmenu",
                 "slider", "switch", "textarea", "authform"],
        "Data": ["accordion", "calendar", "carousel", "table", "tree", "timeline"],
        "Navigation": ["breadcrumb", "commandpalette", "pagination", "stepper", "tabs"],
        "Overlays": ["contextmenu", "drawer", "dropdownmenu", "modal", "popover", "slideover", "tooltip"],
        "Feedback": ["alert", "badge", "banner", "empty", "error", "progress", "skeleton", "toast"],
        "Layout": ["app", "card", "container", "main", "scrollarea", "separator"],
        "Media": ["avatar", "avatargroup", "chip", "collapsible", "icon", "kbd", "link", "user", "marquee"],
        "ColorMode": ["colormodeavatar", "colormodebutton", "colormodeimage", "colormodeselect",
                      "colormodeswitch", "localeselect"],
        "Dashboard": ["dashboardgroup", "dashboardnavbar", "dashboardpanel", "dashboardresizehandle",
                      "dashboardsearchbutton", "dashboardsearch", "dashboardsidebarcollapse",
                      "dashboardsidebartoggle", "dashboardsidebar", "dashboardtoolbar"],
        "Page": ["page", "pageanchors", "pageaside", "pagebody", "pagecard", "pagecolumns",
                 "pagecta", "pagefeature", "pagegrid", "pageheader", "pagehero", "pagelinks",
                 "pagelist", "pagelogos", "pagesection"],
        "Header/Footer": ["header", "footer", "footercolumns"],
        "Blog": ["blogpost", "blogposts"],
        "Changelog": ["changelogversion", "changelogversions"],
        "Chat": ["chatmessage", "chatmessages", "chatpalette", "chatprompt", "chatpromptsubmit"],
        "Editor": ["editor", "editordraghandle", "editoremojimenu", "editormentionmenu",
                   "editorsuggestionmenu", "editortoolbar"],
        "Content": ["contentsearchbutton", "contentsearch", "contentsurround", "contenttoc"],
        "Pricing": ["pricingplan", "pricingplans", "pricingtable"],
    }

    for category, comps in categories.items():
        print(f"{category}:")
        for comp in comps:
            print(f"  - {comp}")
        print()


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    if args[0] == "--status":
        show_status()
    elif args[0] == "--update-all":
        force = "--force" in args
        update_all(force)
    elif args[0] == "--list":
        list_components()
    elif args[0].startswith("-"):
        print(f"Unknown option: {args[0]}")
        print(__doc__)
        sys.exit(1)
    else:
        component = args[0]
        force = "--force" in args
        content = fetch_component(component, force)
        if content:
            print(f"\n# {component} Component\n")
            print(content)
        else:
            print(f"Could not find documentation for: {component}")
            print("\nUse --list to see available components")
            sys.exit(1)


if __name__ == "__main__":
    main()
