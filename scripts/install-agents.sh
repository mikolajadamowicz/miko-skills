#!/usr/bin/env bash
# Installs the review subagents. Skills are installed separately with `npx skills add`.
# Usage: scripts/install-agents.sh [--claude | --cursor | --opencode | --all] [project-dir]
#   --claude    (default) .claude/agents — Claude Code, and Cursor via its .claude/agents support
#   --cursor    .cursor/agents
#   --opencode  .opencode/agents (project) or ~/.config/opencode/agents, converted to OpenCode frontmatter
#   --all       all three
# Without project-dir, installs under $HOME.
set -euo pipefail

target=claude
case "${1:-}" in
  --claude | --cursor | --opencode | --all) target="${1#--}"; shift ;;
esac
project="${1:-}"
root="${project:-$HOME}"
src="$(cd "$(dirname "$0")/../agents" && pwd)"
count="$(ls "$src"/*.md | wc -l | tr -d ' ')"

copy_to() {
  mkdir -p "$1"
  cp "$src"/*.md "$1"/
  echo "Installed $count agents to $1"
}

# OpenCode names agents by filename, reads `mode` and `permission`, and passes
# unknown frontmatter keys to the model provider, so only known keys are written.
opencode_to() {
  mkdir -p "$1"
  for f in "$src"/*.md; do
    awk '
      NR == 1 && $0 == "---" { fm = 1; next }
      fm && $0 == "---" {
        print "---"
        print "description: " desc
        print "mode: subagent"
        if (readonly) { print "permission:"; print "  edit: deny" }
        print "---"
        fm = 0; next
      }
      fm && /^description: / { desc = substr($0, 14) }
      fm && /^readonly: true/ { readonly = 1 }
      !fm { print }
    ' "$f" > "$1/$(basename "$f")"
  done
  echo "Installed $count agents to $1 (OpenCode format)"
}

opencode_dir() {
  if [ -n "$project" ]; then echo "$project/.opencode/agents"; else echo "$HOME/.config/opencode/agents"; fi
}

case "$target" in
  claude) copy_to "$root/.claude/agents" ;;
  cursor) copy_to "$root/.cursor/agents" ;;
  opencode) opencode_to "$(opencode_dir)" ;;
  all)
    copy_to "$root/.claude/agents"
    copy_to "$root/.cursor/agents"
    opencode_to "$(opencode_dir)"
    ;;
esac
