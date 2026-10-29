#!/usr/bin/env bash
# Copies the review subagents. Skills are installed separately with `npx skills add`.
# Usage: scripts/install-agents.sh [--claude | --cursor | --all] [project-dir]
#   --claude  (default) .claude/agents — Claude Code, and Cursor via its .claude/agents compatibility
#   --cursor  .cursor/agents
#   --all     both
# Without project-dir, installs under $HOME.
set -euo pipefail

target=claude
case "${1:-}" in
  --claude | --cursor | --all) target="${1#--}"; shift ;;
esac
root="${1:-$HOME}"

src="$(cd "$(dirname "$0")/../agents" && pwd)"
dirs=()
case "$target" in
  claude) dirs=("$root/.claude/agents") ;;
  cursor) dirs=("$root/.cursor/agents") ;;
  all) dirs=("$root/.claude/agents" "$root/.cursor/agents") ;;
esac

for dest in "${dirs[@]}"; do
  mkdir -p "$dest"
  cp "$src"/*.md "$dest"/
  echo "Installed $(ls "$src"/*.md | wc -l | tr -d ' ') agents to $dest"
done
