---
paths: "server/**/*.ts"
---

# Backend Development Rules

## Directory Structure

```
server/
├── api/              # API routes (auto-registered)
│   ├── fs/           # File system operations
│   ├── tasks/        # Task CRUD
│   ├── agents/       # Agent CRUD + runs + stats
│   └── conversations/ # Chat conversation history
├── routes/           # WebSocket and special routes
│   ├── terminal.ts   # PTY WebSocket
│   ├── notifications.ts
│   └── _ws/          # WebSocket routes that share names with pages
│       └── chat.ts   # Chat WebSocket (Claude Agent SDK bridge)
├── services/         # Business logic
│   ├── agent-executor.ts
│   └── cron-scheduler.ts
├── db/               # Drizzle ORM (schema, migrations, seed)
├── plugins/          # Nitro startup plugins
├── utils/            # Server utilities (singletons, helpers)
└── middleware/       # Server middleware (auth, etc.)
```

### WebSocket Route Collision Rule

Nitro `server/routes/` takes precedence over Nuxt pages. If a WebSocket
handler shares a name with a page route (e.g., `/chat`), place it under
`server/routes/_ws/` to avoid blocking the page. The client connects to
`/_ws/chat` instead of `/chat`.

### Server Imports

Use `~~/server/` aliases for imports within server code, not relative paths:

```typescript
// Good
import { getDb } from '~~/server/db'
import { chatSessionManager } from '~~/server/utils/chat-session-manager'

// Bad
import { getDb } from '../db'
```

## Types

Import shared types from `shared/types/`:

```typescript
import type { Task, FileEntry, ApiResponse } from '~~/shared/types'
```

Never duplicate type definitions - if a type is needed by both frontend and backend, it belongs in `shared/types/`.

## API Route Patterns

### Naming Convention
- `GET` → `*.get.ts`
- `POST` → `*.post.ts`
- `PUT` → `*.put.ts`
- `DELETE` → `*.delete.ts`

### Response Format

Always return consistent API responses:

```typescript
// Success
return { data: result }

// Error
throw createError({
  statusCode: 400,
  message: 'Descriptive error message'
})
```

### Input Validation

Validate request bodies at the start of handlers:

```typescript
export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  if (!body.path || typeof body.path !== 'string')
    throw createError({ statusCode: 400, message: 'path is required' })

  // ... rest of handler
})
```

## Error Handling

- Use `createError()` for HTTP errors
- Include meaningful error messages
- Log server errors but don't expose internals to clients

## Path Security

All file operations must validate paths stay within allowed directories:

```typescript
import { validatePath } from '~~/server/utils/path-validator'

const safePath = validatePath(userProvidedPath) // throws if invalid
```

## Environment Variables

Access via `process.env` or `useRuntimeConfig()`:

```typescript
const config = useRuntimeConfig()
const dbUrl = config.databaseUrl
```

Required env vars should be validated at startup, not per-request.
