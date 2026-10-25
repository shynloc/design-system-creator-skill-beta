#!/usr/bin/env bash
set -euo pipefail
REPO_NAME="${1:-design-system-creator-skill-beta}"
DESCRIPTION="A multimodal, evidence-bound Agent Skill that turns personal taste into a reusable Design Kernel and creates consistent Web, DOCX, PPTX, XLSX, PDF and chart experiences."
command -v git >/dev/null || { echo "git is required" >&2; exit 3; }
command -v gh >/dev/null || { echo "GitHub CLI (gh) is required" >&2; exit 3; }
gh auth status
if [ ! -d .git ]; then git init; fi
git add .
if ! git diff --cached --quiet; then git commit -m "Release Design System Creator 1.0.0-beta.1"; fi
git branch -M main
gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --source . --remote origin --push
