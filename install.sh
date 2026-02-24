#!/usr/bin/env bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}🦾 ValiBjorn${NC} — Hyperthreaded multi-agent startup validation"
echo "https://github.com/montenegronyc/valibjorn"
echo ""

# ── Dependency checks ─────────────────────────────────────────────────────────

check() {
  if command -v "$1" &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} $1"
    return 0
  else
    echo -e "  ${RED}✗${NC} $1 not found"
    return 1
  fi
}

echo "Checking dependencies..."
check python3 || { echo -e "\n${RED}Python 3.10+ is required.${NC} Install from https://python.org"; exit 1; }
check git    || { echo -e "\n${RED}git is required.${NC}"; exit 1; }

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
  echo -e "\n${RED}Python 3.10+ required (found $PYTHON_VERSION).${NC}"
  exit 1
fi
echo -e "  ${GREEN}✓${NC} Python $PYTHON_VERSION"

# ── Install location ──────────────────────────────────────────────────────────

INSTALL_DIR="${VALIBJORN_DIR:-$HOME/.claude/valibjorn}"
SKILLS_DIR="$HOME/.claude/skills"
SETTINGS_FILE="$HOME/.claude/settings.json"

echo ""
echo "Install directory: ${BLUE}$INSTALL_DIR${NC}"

# ── Clone or update ───────────────────────────────────────────────────────────

if [ -d "$INSTALL_DIR/.git" ]; then
  echo ""
  echo "Updating existing installation..."
  git -C "$INSTALL_DIR" pull --quiet
  echo -e "  ${GREEN}✓${NC} Updated"
else
  echo ""
  echo "Cloning ValiBjorn..."
  git clone --quiet https://github.com/montenegronyc/valibjorn.git "$INSTALL_DIR"
  echo -e "  ${GREEN}✓${NC} Cloned"
fi

# ── Python dependencies ───────────────────────────────────────────────────────

echo ""
echo "Installing Python dependencies..."
pip3 install --quiet -r "$INSTALL_DIR/requirements.txt"
echo -e "  ${GREEN}✓${NC} mcp installed"

# ── Copy skills ───────────────────────────────────────────────────────────────

echo ""
echo "Installing Claude Code skill..."
mkdir -p "$SKILLS_DIR"
cp -r "$INSTALL_DIR/skills/valibjorn" "$SKILLS_DIR/"
echo -e "  ${GREEN}✓${NC} Skill installed to $SKILLS_DIR/valibjorn"

# ── Update settings.json ──────────────────────────────────────────────────────

echo ""
echo "Configuring MCP server in $SETTINGS_FILE..."

python3 - <<PYEOF
import json, os, sys

settings_file = "$SETTINGS_FILE"
install_dir   = "$INSTALL_DIR"

# Load or create settings
if os.path.exists(settings_file):
    with open(settings_file, "r") as f:
        try:
            settings = json.load(f)
        except json.JSONDecodeError:
            print("  ⚠  Could not parse settings.json — creating backup and starting fresh")
            os.rename(settings_file, settings_file + ".bak")
            settings = {}
else:
    os.makedirs(os.path.dirname(settings_file), exist_ok=True)
    settings = {}

# Inject MCP server config
settings.setdefault("mcpServers", {})["valibjorn"] = {
    "command": "python3",
    "args": ["-m", "src.mcp.server"],
    "cwd": install_dir
}

with open(settings_file, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print(f"  \033[0;32m✓\033[0m MCP server configured")
PYEOF

# ── Done ──────────────────────────────────────────────────────────────────────

echo ""
echo -e "${GREEN}${BOLD}✅ ValiBjorn installed successfully!${NC}"
echo ""
echo -e "  ${BOLD}Restart Claude Code${NC} to activate the MCP server, then say:"
echo ""
echo -e "    ${BLUE}\"validate my idea: [describe your startup concept]\"${NC}"
echo -e "    ${BLUE}\"valibjorn\"${NC}"
echo ""
