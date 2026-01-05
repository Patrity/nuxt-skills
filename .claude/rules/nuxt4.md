---
paths: "**/*.vue,**/nuxt.config.ts,app/**/*,server/**/*"
---

# Nuxt 4 Development Rules

## Directory Structure (Nuxt 4)

Nuxt 4 uses `app/` as the source root. This is different from Nuxt 3.

```
project/
├── app/                    # Source root (NEW in Nuxt 4)
│   ├── components/
│   ├── composables/
│   ├── layouts/
│   ├── middleware/
│   ├── pages/
│   ├── plugins/
│   ├── assets/
│   ├── app.vue
│   └── error.vue
├── shared/                 # Shared between app and server (NEW)
│   ├── types/
│   └── utils/
├── server/                 # Stays at project root
│   ├── api/
│   ├── middleware/
│   └── utils/
├── public/
├── nuxt.config.ts
└── package.json
```

## Import Aliases

- `~/` or `@/` - resolves to `app/` directory
- `~~/` or `@@/` - resolves to project root
- `#imports` - auto-imports
- `#components` - component auto-imports

## Component Patterns

- Always use `<script setup lang="ts">`
- Use `defineProps<T>()` with TypeScript interfaces
- Use `defineEmits<T>()` for typed events
- Use `withDefaults()` for prop defaults

```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

const emit = defineEmits<{
  update: [value: number]
}>()
</script>
```

## Data Fetching

- Use `useFetch()` for simple requests
- Use `useAsyncData()` for complex scenarios
- Use `$fetch` for client-side only requests
- Always handle loading and error states

## Auto-imports

These are auto-imported (don't manually import):
- Vue: `ref`, `reactive`, `computed`, `watch`, `onMounted`, etc.
- Nuxt: `useFetch`, `useAsyncData`, `useRoute`, `useRouter`, `useState`
- Components in `app/components/`
- Composables in `app/composables/`

## Skills Reference

Three skills are available for Nuxt development:

### Nuxt Framework (`nuxt-docs`)
Use for Nuxt core concepts: composables, routing, config, deployment.

```bash
python3 .claude/skills/nuxt-docs/fetch.py usefetch
python3 .claude/skills/nuxt-docs/fetch.py routing
python3 .claude/skills/nuxt-docs/fetch.py deployment
```

### Nuxt UI Components (`nuxt-ui-docs`)
Use for Nuxt UI component APIs: props, slots, events.

```bash
python3 .claude/skills/nuxt-ui-docs/fetch.py button
python3 .claude/skills/nuxt-ui-docs/fetch.py modal
```

### Implementation Examples (`nuxt-ui-templates`)
Use for real-world patterns: dashboards, landing pages, SaaS apps.

```bash
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard --structure
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard app/layouts/default.vue
```

## Complex Frontend Tasks

For multi-step features (dashboards, auth flows, full pages), follow this workflow:

### 1. Check existing patterns
```bash
# See how the template structures it
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard --structure
python3 .claude/skills/nuxt-ui-templates/fetch.py dashboard app/layouts/default.vue
```

### 2. Understand the components needed
```bash
# Fetch API docs for components you'll use
python3 .claude/skills/nuxt-ui-docs/fetch.py dashboardsidebar
python3 .claude/skills/nuxt-ui-docs/fetch.py dashboardpanel
```

### 3. Check Nuxt patterns if needed
```bash
# For routing, data fetching, etc.
python3 .claude/skills/nuxt-docs/fetch.py routing
python3 .claude/skills/nuxt-docs/fetch.py usefetch
```

### 4. Implement iteratively
- Start with layout/structure
- Add components one at a time
- Wire up data fetching
- Add interactivity

### Example: "Build a dashboard"
1. `nuxt-ui-templates dashboard --structure` → see file organization
2. `nuxt-ui-templates dashboard app/layouts/default.vue` → get layout pattern
3. `nuxt-ui-docs dashboardsidebar` → understand sidebar props
4. Implement layout in `app/layouts/dashboard.vue`
5. Add pages under `app/pages/`
