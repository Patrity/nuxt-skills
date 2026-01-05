---
name: nuxt-ui
description: Fetches Nuxt UI v4 component documentation from GitHub. Use when building UI with Nuxt UI, needing component APIs, props, slots, or usage examples.
allowed-tools: Bash, Read, WebFetch
---

# Nuxt UI v4 Documentation Skill

Fetches up-to-date Nuxt UI v4 docs from the official GitHub repository.

## Usage

### Fetch a specific component's docs

```bash
python3 .claude/skills/nuxt-ui-docs/fetch.py <ComponentName>
```

Examples:
```bash
python3 .claude/skills/nuxt-ui-docs/fetch.py Button
python3 .claude/skills/nuxt-ui-docs/fetch.py Modal
python3 .claude/skills/nuxt-ui-docs/fetch.py Form
```

### Update all cached docs

```bash
python3 .claude/skills/nuxt-ui-docs/fetch.py --update-all
```

### Check what's cached

```bash
python3 .claude/skills/nuxt-ui-docs/fetch.py --status
```

## Cache System

- Docs are cached in `.claude/skills/nuxt-ui-docs/cache/`
- Manifest at `.claude/skills/nuxt-ui-docs/manifest.json` tracks:
  - Last fetch timestamp per component
  - GitHub commit SHA at time of fetch
- Use `--force` to bypass cache and fetch fresh

## Quick Reference

Read the cached quick reference for common patterns:
- [cache/quick-reference.md](cache/quick-reference.md)

## Source

Docs fetched from: https://github.com/nuxt/ui/tree/v4/docs/content/docs

## When to Use

- "What props does UButton accept?"
- "How do I use UForm with validation?"
- "Show me UTable examples"
- "What slots does UModal have?"
