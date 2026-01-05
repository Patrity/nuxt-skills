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

Rules in `.claude/rules/` auto-load for `.vue` files and contain conventions. Read them, but fetch skills for API details.

## Commands
- `pnpm dev` - development server
- `pnpm build` - production build
- `pnpm lint` - lint code
