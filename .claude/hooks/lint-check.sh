#!/bin/bash
# Post-edit hook: Run lint on modified files
# Exit 0 = success, Exit 2 = block with message to Claude

cd "$CLAUDE_PROJECT_DIR" || exit 1

# Run lint check
if ! pnpm -w lint --quiet 2>/dev/null; then
  echo "Lint errors found. Please fix them before continuing." >&2
  exit 2
fi

exit 0
