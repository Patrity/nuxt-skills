# Claude Code Setup for Nuxt 4 + Nuxt UI v4

A ready-to-use Claude Code configuration for Nuxt 4 and Nuxt UI v4 development. Solves the problem of LLM knowledge cutoff by fetching current documentation on-demand.

## Why This Exists

Claude's training data doesn't include Nuxt 4 or Nuxt UI v4. This setup:

- **Forces** Claude to fetch current docs before writing code
- **Caches** documentation locally with smart invalidation
- **Keeps context low** by loading docs on-demand, not preloading
- **Provides conventions** via auto-loading rules for `.vue` files

## Requirements

- **Python 3** - Required for running fetch scripts
- **curl** - Used for fetching docs from GitHub (pre-installed on macOS/Linux)

## Quick Start

### Option 1: Copy to Your Project

```bash
# Clone this repo
git clone https://github.com/yourusername/claude-nuxt-setup.git

# Copy .claude directory to your project
cp -r claude-nuxt-setup/.claude /path/to/your/nuxt-project/
```

### Option 2: Use as Template

Click "Use this template" on GitHub to create a new repo with this setup.

## Structure

```
.claude/
├── CLAUDE.md                    # Main instructions (forces skill usage)
├── rules/
│   ├── nuxt4.md                 # Nuxt 4 conventions (auto-loads for .vue)
│   └── nuxt-ui.md               # Nuxt UI conventions (auto-loads for .vue)
└── skills/
    ├── nuxt-docs/               # Nuxt framework documentation
    │   ├── SKILL.md
    │   ├── fetch.py
    │   ├── manifest.json
    │   └── cache/
    ├── nuxt-ui-docs/            # Nuxt UI v4 component APIs
    │   ├── SKILL.md
    │   ├── fetch.py
    │   ├── manifest.json
    │   └── cache/
    └── nuxt-ui-templates/       # Real implementation examples
        ├── SKILL.md
        ├── fetch.py
        └── cache/
```

> **Tip**: Add `.claude/skills/*/cache/` to your `.gitignore` so cached docs aren't committed. Users will fetch fresh docs on first use.

## How It Works

### Rules (Auto-loaded)

Rules in `.claude/rules/` automatically load when editing matching files:

- `nuxt4.md` → Loads for `**/*.vue`, `**/nuxt.config.ts`, `app/**/*`
- `nuxt-ui.md` → Loads for `**/*.vue`

These provide conventions like directory structure, component patterns, and theming rules.

### Skills (On-demand)

Skills fetch current documentation from GitHub when invoked:

```bash
# Nuxt framework docs (composables, routing, config)
python3 .claude/skills/nuxt-docs/fetch.py usefetch
python3 .claude/skills/nuxt-docs/fetch.py routing

# Nuxt UI component APIs (props, slots, events)
python3 .claude/skills/nuxt-ui-docs/fetch.py button
python3 .claude/skills/nuxt-ui-docs/fetch.py dashboardsidebar

# Real implementation examples
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard --structure
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard app/layouts/default.vue
```

### Caching

- Docs are cached for 24 hours
- Manifest tracks last fetch time and GitHub commit SHA
- Use `--force` to bypass cache
- Use `--status` to check cache state

```bash
# Check what's cached
python3 .claude/skills/nuxt-ui-docs/fetch.py --status

# Force refresh
python3 .claude/skills/nuxt-ui-docs/fetch.py button --force

# Update all cached components
python3 .claude/skills/nuxt-ui-docs/fetch.py --update-all
```

## Available Commands

### nuxt-docs

```bash
python3 .claude/skills/nuxt-docs/fetch.py --list      # List all topics
python3 .claude/skills/nuxt-docs/fetch.py <topic>     # Fetch topic
python3 .claude/skills/nuxt-docs/fetch.py --status    # Cache status
```

Topics: `usefetch`, `useasyncdata`, `routing`, `configuration`, `deployment`, `state-management`, etc.

### nuxt-ui-docs

```bash
python3 .claude/skills/nuxt-ui-docs/fetch.py --list       # List all components
python3 .claude/skills/nuxt-ui-docs/fetch.py <component>  # Fetch component
python3 .claude/skills/nuxt-ui-docs/fetch.py --status     # Cache status
python3 .claude/skills/nuxt-ui-docs/fetch.py --update-all # Update cached
```

Components: 100+ including `button`, `modal`, `form`, `table`, `dashboardsidebar`, `dashboardpanel`, `pagehero`, `chatmessage`, `editor`, etc.

### nuxt-ui-templates

```bash
python3 .claude/skills/nuxt-ui-templates/fetch.py --list              # List templates
python3 .claude/skills/nuxt-ui-templates/fetch.py <template> --structure  # Show structure
python3 .claude/skills/nuxt-ui-templates/fetch.py <template> <file>   # Fetch file
```

Templates: `dashboard`, `saas`, `landing`, `chat`, `docs`, `portfolio`, `editor`, `changelog`, `starter`

## Customization

### Adding Project-Specific Rules

Create new rule files in `.claude/rules/`:

```markdown
---
paths: "app/components/custom/**/*.vue"
---

# Custom Component Rules

Your project-specific conventions here...
```

### Adjusting Cache TTL

Edit `CACHE_TTL_HOURS` in each `fetch.py`:

```python
CACHE_TTL_HOURS = 24  # Change to desired hours
```

### Adding New Components

If Nuxt UI adds new components, add them to `COMPONENT_PATHS` in `nuxt-ui-docs/fetch.py`:

```python
COMPONENT_PATHS = {
    # ...existing components...
    "newcomponent": "new-component.md",
}
```

## Updating Documentation Sources

### When Nuxt UI Updates

```bash
# Clear cache and refetch
rm -rf .claude/skills/nuxt-ui-docs/cache/*
python3 .claude/skills/nuxt-ui-docs/fetch.py button  # Will fetch fresh
```

### When Nuxt Updates

```bash
rm -rf .claude/skills/nuxt-docs/cache/*
python3 .claude/skills/nuxt-docs/fetch.py usefetch
```

### Bulk Update

```bash
# Update all cached Nuxt UI docs
python3 .claude/skills/nuxt-ui-docs/fetch.py --update-all --force
```

## Contributing

### Adding New Skills

1. Create directory: `.claude/skills/your-skill/`
2. Add `SKILL.md` with frontmatter:
   ```markdown
   ---
   name: your-skill
   description: What this skill does. When to use it.
   allowed-tools: Bash, Read
   ---
   ```
3. Add `fetch.py` with caching logic
4. Add `manifest.json` for tracking

### Improving Rules

1. Edit files in `.claude/rules/`
2. Test with Claude Code on sample tasks
3. Keep rules concise - details should be in skills

### Reporting Issues

- Missing components? Open an issue with the component name
- Incorrect docs path? Check the Nuxt UI GitHub structure
- Cache issues? Try `--force` flag first

## License

MIT

## References

- [Nuxt](https://nuxt.com) - The framework
- [Nuxt UI](https://ui.nuxt.com) - The component library
- [Claude Code](https://claude.ai/claude-code) - The AI coding assistant
- [Claude Skills Docs](https://code.claude.com/docs/en/skills) - Documentation on how to create skills
