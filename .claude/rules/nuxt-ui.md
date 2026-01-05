---
paths: "**/*.vue"
---

# Nuxt UI v4 Rules

## Component Usage

Always prefer Nuxt UI components over custom implementations:
- Buttons: `<UButton>` not `<button>`
- Inputs: `<UInput>`, `<UTextarea>`, `<USelect>`
- Layout: `<UCard>`, `<UContainer>`, `<UDivider>`
- Feedback: `<UAlert>`, `<UBadge>`, `<UToast>`
- Overlays: `<UModal>`, `<UDrawer>`, `<UPopover>`
- Navigation: `<UTabs>`, `<UBreadcrumb>`, `<UPagination>`
- Data: `<UTable>`, `<UAccordion>`

## Prop Conventions

Colors (semantic):
- `primary`, `secondary`, `success`, `warning`, `error`, `info`, `neutral`

Sizes:
- `xs`, `sm`, `md`, `lg`, `xl`

Variants (component-specific):
- Button: `solid`, `outline`, `soft`, `ghost`, `link`
- Badge: `solid`, `outline`, `soft`, `subtle`

## Icons

Nuxt UI uses Iconify. Common pattern:
```vue
<UButton icon="i-heroicons-plus-20-solid" />
<UButton trailing-icon="i-heroicons-arrow-right-20-solid" />
```

Icon format: `i-{collection}-{name}-{size}-{style}`
- Collections: `heroicons`, `lucide`, `simple-icons`
- Sizes: `16`, `20`, `24`
- Styles: `solid`, `outline`

Always prefer lucide icons, if possible

## Forms

```vue
<UForm :state="state" :schema="schema" @submit="onSubmit">
  <UFormField label="Email" name="email">
    <UInput v-model="state.email" type="email" />
  </UFormField>
  <UButton type="submit">Submit</UButton>
</UForm>
```

Use Zod for schema validation:
```ts
import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Invalid email')
})
```

## Theming
Never use tailwindcss dark mode classes. NuxtUI handles this out of the box within the theme.
Colors are configured in `app.config.ts`:
```ts
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'green',
      neutral: 'slate'
    }
  }
})
```

## Skills Reference

Two skills are available for Nuxt UI development:

### Component API (`nuxt-ui-docs`)
Use when you need:
- Props, slots, events for a specific component
- TypeScript types and interfaces
- Component configuration options
- Validation patterns

```bash
python3 .claude/skills/nuxt-ui-docs/fetch.py <component>
# Examples: button, modal, dashboardsidebar, authform
```

### Implementation Examples (`nuxt-ui-templates`)
Use when you need:
- How to compose multiple components together
- Real-world layout patterns (dashboards, landing pages)
- File structure and organization patterns
- Complete working examples

```bash
python3 .claude/skills/nuxt-ui-templates/fetch.py <template> --structure
python3 .claude/skills/nuxt-ui-templates/fetch.py <template> <file_path>
# Templates: dashboard, saas, landing, chat, docs, portfolio
```

### When to Use Which

| Question | Skill |
|----------|-------|
| "What props does UButton accept?" | `nuxt-ui-docs` |
| "How do I set up a dashboard layout?" | `nuxt-ui-templates` |
| "What events does UTable emit?" | `nuxt-ui-docs` |
| "Show me a real sidebar implementation" | `nuxt-ui-templates` |
| "How do I validate a form with Zod?" | `nuxt-ui-docs` (form) |
| "How do I structure a SaaS pricing page?" | `nuxt-ui-templates` (saas) |
