#!/usr/bin/env bash
# Installs the review subagents. Skills are installed separately with `npx skills add`.
# Usage: scripts/install-agents.sh [--claude | --cursor | --cursor-plugin | --opencode | --all] [project-dir]
#   --claude         (default) .claude/agents — Claude Code, and the Cursor editor via its .claude/agents support
#   --cursor         .cursor/agents
#   --cursor-plugin  ~/.cursor/plugins/local/miko-skills-agents, a plugin that holds only the agents. For the
#                    Cursor CLI, which loaded agents only from plugins when tested with cursor-agent 2026.11.17.
#   --opencode       .opencode/agents (project) or ~/.config/opencode/agents, converted to OpenCode frontmatter
#   --all            .claude, .cursor, and OpenCode, without --cursor-plugin
# Without project-dir, installs under $HOME.
set -euo pipefail

target=claude
case "${1:-}" in
  --claude | --cursor | --cursor-plugin | --opencode | --all) target="${1#--}"; shift ;;
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

# Cursor ignores symlinks in plugins/local, so the files are copied. The plugin has no skills
# folder, so skills installed with `npx skills` do not load twice.
cursor_plugin_to() {
  local version
  version="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$src/../.cursor-plugin/plugin.json")"
  rm -rf "$1"
  mkdir -p "$1/.cursor-plugin"
  copy_to "$1/agents"
  cat > "$1/.cursor-plugin/plugin.json" <<EOF
{
  "name": "miko-skills-agents",
  "version": "$version",
  "description": "miko-skills reviewer agents only. Install the skills with npx skills.",
  "agents": "./agents/"
}
EOF
  echo "Installed the Cursor plugin $1. Start a new cursor-agent session to load it."
}

opencode_dir() {
  if [ -n "$project" ]; then echo "$project/.opencode/agents"; else echo "$HOME/.config/opencode/agents"; fi
}

case "$target" in
  claude) copy_to "$root/.claude/agents" ;;
  cursor) copy_to "$root/.cursor/agents" ;;
  cursor-plugin)
    [ -z "$project" ] || { echo "--cursor-plugin installs under ~/.cursor/plugins/local and takes no project-dir." >&2; exit 2; }
    cursor_plugin_to "$HOME/.cursor/plugins/local/miko-skills-agents"
    ;;
  opencode) opencode_to "$(opencode_dir)" ;;
  all)
    copy_to "$root/.claude/agents"
    copy_to "$root/.cursor/agents"
    opencode_to "$(opencode_dir)"
    ;;
esac
