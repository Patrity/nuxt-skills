# Sample CLAUDE.md for Nuxt 4 + Nuxt UI v4 Projects

Copy the relevant sections below into your project's `.claude/CLAUDE.md`.

---

## Recommended Version

```markdown
# Project

Nuxt 4 + Nuxt UI v4 frontend.

## Stack
- Nuxt 4 (app/ directory structure)
- Nuxt UI v4
- TypeScript
- Zod for validation

## IMPORTANT: Knowledge Cutoff

Your knowledge of Nuxt 4 and Nuxt UI v4 is OUTDATED. Do NOT rely on training data for:
- Nuxt 4 APIs, directory structure, or composables
- Nuxt UI v4 component props, slots, or patterns
- Implementation examples

ALWAYS use the skills below to fetch current documentation before writing code.

## Required Skills Usage

### Before using any Nuxt composable:
```bash
python3 .claude/skills/nuxt-docs/fetch.py <topic>
# Examples: usefetch, routing, deployment, configuration
```

### Before using any Nuxt UI component:
```bash
python3 .claude/skills/nuxt-ui-docs/fetch.py <component>
# Examples: button, modal, form, dashboardsidebar
```

### Before building layouts or complex features:
```bash
python3 .claude/skills/nuxt-ui-templates/fetch.py <template> --structure
python3 .claude/skills/nuxt-ui-templates/fetch.py <template> <file_path>
# Templates: dashboard, saas, landing, chat, docs, portfolio
```

## Rules

Rules in `.claude/rules/` auto-load for `.vue` files and contain conventions.

## Commands
- `pnpm dev` - development server
- `pnpm build` - production build
- `pnpm lint` - lint code
```

---

## Required Files

Copy these directories to new projects:
```
.claude/
├── CLAUDE.md           # Project instructions (use template above)
├── rules/
│   ├── nuxt4.md        # Nuxt 4 patterns & directory structure
│   └── nuxt-ui.md      # Nuxt UI component conventions
└── skills/
    ├── nuxt-docs/      # Nuxt framework documentation fetcher
    ├── nuxt-ui-docs/   # Nuxt UI component API fetcher
    └── nuxt-ui-templates/  # Real implementation examples
```

## Key Points

1. **Force skill usage** - Language like "ALWAYS use" and "Do NOT rely on training data"
2. **Knowledge cutoff warning** - Explicitly state the LLM's knowledge is outdated
3. **Specific triggers** - "Before using any Nuxt composable", "Before using any Nuxt UI component"
4. **Rules are conventions** - Skills are for API details
5. **Keep CLAUDE.md brief** - Details live in rules files
