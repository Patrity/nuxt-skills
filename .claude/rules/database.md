---
paths: "db/**/*.ts,drizzle.config.ts,server/db/**/*.ts"
---

# Database Rules (Drizzle ORM)

## Directory Structure

```
db/
├── schema/           # Table definitions
│   ├── tasks.ts
│   ├── reminders.ts
│   └── index.ts      # Re-exports all schemas
├── migrations/       # Generated migrations (don't edit manually)
├── index.ts          # DB client export
└── seed.ts           # Optional seed data
```

## Schema Definition

Define tables in `db/schema/`:

```typescript
import { pgTable, uuid, text, timestamp, integer } from 'drizzle-orm/pg-core'

export const tasks = pgTable('tasks', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: text('title').notNull(),
  status: text('status').default('todo'),
  priority: integer('priority').default(0),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow()
})
```

## Type Export Workflow

When adding/modifying schemas, sync types to `shared/types/`:

1. Define schema in `db/schema/*.ts`
2. Run `pnpm drizzle-kit generate` to create migration
3. Export inferred types or update `shared/types/index.ts` manually

```typescript
// db/schema/tasks.ts
import { InferSelectModel, InferInsertModel } from 'drizzle-orm'

export type Task = InferSelectModel<typeof tasks>
export type NewTask = InferInsertModel<typeof tasks>
```

## Migration Workflow

### Generate migration after schema changes:
```bash
pnpm drizzle-kit generate
```

### Apply migrations:
```bash
pnpm drizzle-kit migrate
```

### Push schema directly (dev only):
```bash
pnpm drizzle-kit push
```

### View database in studio:
```bash
pnpm drizzle-kit studio
```

## Query Patterns

Use Drizzle's query builder:

```typescript
import { db } from '~~/db'
import { tasks } from '~~/db/schema'
import { eq, desc } from 'drizzle-orm'

// Select
const allTasks = await db.select().from(tasks)
const task = await db.select().from(tasks).where(eq(tasks.id, id))

// Insert
const [newTask] = await db.insert(tasks).values({ title }).returning()

// Update
await db.update(tasks).set({ status: 'done' }).where(eq(tasks.id, id))

// Delete
await db.delete(tasks).where(eq(tasks.id, id))
```

## Connection

Use Neon serverless driver:

```typescript
// db/index.ts
import { neon } from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'
import * as schema from './schema'

const sql = neon(process.env.DATABASE_URL!)
export const db = drizzle(sql, { schema })
```

## Important

- Never edit files in `db/migrations/` manually
- Always generate migrations for schema changes
- Keep `shared/types/` in sync with schema changes
- Use transactions for multi-table operations
