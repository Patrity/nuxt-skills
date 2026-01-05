---
name: nuxt-ui-templates
description: Fetches real-world Nuxt UI template examples from nuxt-ui-templates org. Use when needing implementation patterns for dashboards, landing pages, SaaS apps, chat interfaces, or how to compose Nuxt UI components together.
allowed-tools: Bash, Read
---

# Nuxt UI Templates Skill

Fetches real implementation examples from the official Nuxt UI templates.

## Available Templates

| Template | Description |
|----------|-------------|
| `dashboard` | Full dashboard with sidebar, panels, navbar |
| `saas` | SaaS app with auth, pricing, landing |
| `landing` | Marketing landing page |
| `chat` | AI chatbot with Vercel AI SDK |
| `docs` | Documentation site |
| `portfolio` | Portfolio/personal site |
| `editor` | Notion-like WYSIWYG editor |
| `changelog` | Changelog/release notes |
| `starter` | Minimal Nuxt starter |

## Usage

### List template structure

```bash
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard --structure
```

### Fetch a specific file

```bash
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard app/layouts/default.vue
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard app/components/UserMenu.vue
python3 .claude/skills/nuxt-ui-templates/fetch.py saas app/pages/pricing.vue
```

### Search for patterns

```bash
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard --search "DashboardSidebar"
```

### List all templates

```bash
python3 .claude/skills/nuxt-ui-templates/fetch.py --list
```

## When to Use

- "How do I set up a dashboard layout?"
- "Show me a real sidebar implementation"
- "How do I structure a SaaS pricing page?"
- "What's the pattern for a chat interface?"
