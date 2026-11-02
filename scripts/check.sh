#!/usr/bin/env bash
# Fails when the files that must agree across harnesses drift. Run before every commit.
set -euo pipefail
cd "$(dirname "$0")/.."

for tool in rg python3; do
  command -v "$tool" >/dev/null || { echo "check.sh needs $tool, which is not on PATH. Nothing was checked." >&2; exit 2; }
done

fail=0
err() { echo "FAIL: $*"; fail=1; }

field() { python3 -c "import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])" "$1" "$2"; }
for key in name version description; do
  [ "$(field .cursor-plugin/plugin.json "$key")" = "$(field .claude-plugin/plugin.json "$key")" ] \
    || err "$key differs between .cursor-plugin/plugin.json and .claude-plugin/plugin.json"
done
plugin="$(field .claude-plugin/plugin.json name)"
marketplace_description="$(python3 -c "import json; print(json.load(open('.claude-plugin/marketplace.json'))['plugins'][0]['description'])")"
[ "$marketplace_description" = "$(field .claude-plugin/plugin.json description)" ] \
  || err "plugin description differs between .claude-plugin/marketplace.json and .claude-plugin/plugin.json"

for dir in skills/*/; do
  skill="$(basename "$dir")"
  name="$(awk '/^name: /{print $2; exit}' "$dir/SKILL.md")"
  [ "$name" = "$skill" ] || err "skills/$skill/SKILL.md has name '$name'; it must match its directory"
  [[ "$skill" == review-* ]] || continue
  rg -q "\`$skill\`" skills/miko-review/SKILL.md || err "skills/miko-review/SKILL.md does not list lens $skill"
  rg -q "^\| \`$skill\` \|" README.md || err "README.md has no table row for lens $skill"
  lens="${skill#review-}"
  rg -q "with \`lens: $lens\`" "$dir/SKILL.md" || err "skills/$skill/SKILL.md does not tell the lens to return lens: $lens"
  [[ "$(field .claude-plugin/plugin.json description)" == *"${lens//-/ }"* ]] \
    || err "plugin description does not mention lens '${lens//-/ }'"
  rg -q 'extensions\.md' "$dir/SKILL.md" || err "skills/$skill/SKILL.md does not load its extensions"
  rg -q -l "^  - $skill$" agents/ >/dev/null || err "no agent in agents/ preloads skill $skill"
done

paths="$(awk '/in the first of these that exists/{print; exit}' agents/truth-reviewer.md | sed 's/.*exists: //')"
for f in agents/*.md; do
  name="$(awk '/^name: /{print $2; exit}' "$f")"
  [ "$name.md" = "$(basename "$f")" ] || err "$f has name '$name'; OpenCode names agents by filename"
  awk '/^---$/{n++; next} n==1' "$f" | rg -q '^description: .+' || err "$f needs a one-line description"
  awk '/^---$/{n++; next} n==1' "$f" | rg -q '^model: inherit$' || err "$f must use model: inherit"
  skill="$(awk '/^skills:/{getline; print $2; exit}' "$f")"
  awk '/^---$/{n++; next} n==1' "$f" | rg -q "^  - $plugin:$skill$" \
    || err "$f preloads $skill but not $plugin:$skill"
  [ "$(awk '/in the first of these that exists/{print; exit}' "$f" | sed 's/.*exists: //')" = "$paths" ] \
    || err "$f skill search paths differ from agents/truth-reviewer.md"
done

[ "$fail" = 0 ] && echo "check: ok"
exit "$fail"
